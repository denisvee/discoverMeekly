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
        public async Task<string> GetTracks()
        {
            var accessToken = Redirect("https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}");
            //var discoverWeeklyTracks = await GetDiscoverWeekly(accessToken.);
            return "succes";
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
