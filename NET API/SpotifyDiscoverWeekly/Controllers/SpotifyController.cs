using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;

namespace SpotifyDiscoverWeekly.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class SpotifyController : ControllerBase
    {
        [HttpGet]
        public async Task<object> GetTracks()
        {
            var accessToken = await AuthenticateSpotify();
            var discoverWeeklyTracks = await GetDiscoverWeekly(accessToken);
            return discoverWeeklyTracks;
        }
        public static async Task<string> AuthenticateSpotify()
        {
            HttpClient client = new HttpClient();
            byte[] grantArray = Encoding.ASCII.GetBytes(Environment.GetEnvironmentVariable("SPOTIFY_AUTH"));
            byte[] authArray = Encoding.ASCII.GetBytes(Environment.GetEnvironmentVariable("SPOTIFY_CLIENT_CREDENTIALS"));
            var authString = Convert.ToBase64String(authArray);
            var grantBody = System.Web.HttpUtility.UrlEncode(grantArray);
            client.DefaultRequestHeaders.Add("Authorizaton", authString);
            using (HttpResponseMessage response = await client.PostAsJsonAsync(Environment.GetEnvironmentVariable("SPOTIFY_AUTH_ENDPOINT"), grantBody))
            {
                var accessToken = await response.Content.ReadAsStringAsync();
                return accessToken;
            }
        }
        public static async Task<object> GetDiscoverWeekly(string accessToken)
        {
            HttpClient client = new HttpClient();
            client.DefaultRequestHeaders.Add("Authorization", accessToken);
            using (HttpResponseMessage response = await client.GetAsync(Environment.GetEnvironmentVariable("SPOTIFY_DISCOVER_TRACKS_ENDPOINT")))
            {
                if (response.StatusCode.Equals(200))
                {
                    Console.WriteLine("Successfuly got Spotify playlist data.");
                    return JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());
                }
                Console.WriteLine("Failed to get Spotify playlist data.");
                return new object();
            }
        }
    }
}
