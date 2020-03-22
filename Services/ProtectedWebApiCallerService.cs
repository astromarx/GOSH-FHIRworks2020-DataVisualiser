using HDR_UK_Web_Application.IServices;
using Microsoft.Identity.Client;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;

namespace HDR_UK_Web_Application.Services
{
    public class ProtectedWebApiCallerService : IProtectedWebApiCallerService
    {
        private readonly IAccessTokenService _authenticationResult;
        private readonly IHttpClientFactory _factory;
        private readonly ILoggerManager _logger;
        private static Dictionary<string, JObject> _cache = new Dictionary<string, JObject>();

        public ProtectedWebApiCallerService(IAccessTokenService authenticationResult, IHttpClientFactory factory, ILoggerManager logger)
        {
            _authenticationResult = authenticationResult;
            _factory = factory;
            _logger = logger;
        }


        public async Task<JObject> ProtectedWebApiCaller(string webApiUrl)
        {
            AuthenticationResult result = await _authenticationResult.GetAuthenticationResult();
            var client = _factory.CreateClient("protectedapi");

            if (result != null)
            {
                client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("bearer", result.AccessToken);
            }
            else
            {
                _logger.LogError("Class: ProtectedWebApiCallerService, Method: ProtectedWebApiCaller, Error: The access token is equal to null.");
                return null;
            }

            try
            {
                if (!_cache.ContainsKey(webApiUrl))
                {
                    HttpResponseMessage response = await client.GetAsync(webApiUrl);
                    string json = await response.Content.ReadAsStringAsync();
                    var res = JsonConvert.DeserializeObject<JObject>(json);
                    _cache[webApiUrl] = res;
                }
                return _cache[webApiUrl];
            }
            catch (Exception ex)
            {
                _logger.LogError($"Class: ProtectedWebApiCallerService, Method: ProtectedWebApiCaller, {Environment.NewLine} Exception: {ex}, {Environment.NewLine} Message: {ex.Message}, {Environment.NewLine} StackTrace: {ex.StackTrace}");
                return null;
            }



        }
    }
}
