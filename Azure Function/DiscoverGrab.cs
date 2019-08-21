using System;
//using Microsoft.Azure.WebJobs;
//using Microsoft.Azure.WebJobs.Host;
using Microsoft.Extensions.Logging;
using System.Net.Http;
using System.Threading.Tasks;
using System.Text;
using Newtonsoft.Json;

namespace Company.Function
{
    public static class DiscoverGrab
    {
        //[FunctionName("DiscoverGrab")]
        public static async Task Run(ILogger log)
        {
            var accessToken = await AuthenticateSpotify();
            await GetDiscoverWeekly(accessToken); //probably store in the queue and reference with another func
            log.LogInformation($"C# Timer trigger function executed at: {DateTime.Now}");
        }
        public static async Task<string> AuthenticateSpotify()
        {
            HttpClient client = new HttpClient();
            byte[] grantArray = Encoding.UTF8.GetBytes(Environment.GetEnvironmentVariable("SPOTIFY_AUTH"));
            byte[] authArray = Encoding.UTF8.GetBytes(Environment.GetEnvironmentVariable("SPOTIFY_CLIENT_CREDENTIALS"));
            var authString = System.Convert.ToBase64String(authArray);
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
