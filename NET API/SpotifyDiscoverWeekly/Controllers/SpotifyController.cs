using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;

namespace SpotifyDiscoverWeekly.Controllers
{
    [Route("/[controller]")]
    [ApiController]
    public class SpotifyController : ControllerBase
    {
        [HttpGet]
        public async Task<IActionResult> GetDiscoverWeeklyTracks()
        {
            var accessToken = await GetSpotifyToken();
            await GetDiscoverWeekly(accessToken.AccessToken);
            return Ok();
        }
        public static async Task<Models.Token> GetSpotifyToken()
        {
            string auth = Convert.ToBase64String(Encoding.UTF8.GetBytes(Environment.GetEnvironmentVariable("SPOTIFY_CLIENT_ID") + ":" + Environment.GetEnvironmentVariable("SPOTIFY_CLIENT_SECRET")));

            List<KeyValuePair<string, string>> args = new List<KeyValuePair<string, string>>
            {
                new KeyValuePair<string, string>("grant_type", "client_credentials")
            };
            HttpClient client = new HttpClient();
            client.DefaultRequestHeaders.Add("Authorization", $"Basic {auth}");
            HttpContent content = new FormUrlEncodedContent(args);

            HttpResponseMessage resp = await client.PostAsync("https://accounts.spotify.com/api/token", content);
            string msg = await resp.Content.ReadAsStringAsync();

            return JsonConvert.DeserializeObject<Models.Token>(msg);
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
