using System;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Extensions.Logging;
using System.Net.Http;
using System.Threading.Tasks;

namespace Company.Function
{
    public static class DiscoverGrab
    {
        [FunctionName("DiscoverGrab")]
        public static void Run([TimerTrigger("0 0 23 * * MON")]TimerInfo myTimer, ILogger log)
        {
            log.LogInformation($"C# Timer trigger function executed at: {DateTime.Now}");
        }

        public static async Task GetDiscoverWeekly()
        {
            HttpClient client = new HttpClient(); 
            Environment.GetEnvironmentVariable("DISCOVER_TRACKS_ENDPOINT");
            HttpResponseMessage response = await client.GetAsync()
        }
    }
}
