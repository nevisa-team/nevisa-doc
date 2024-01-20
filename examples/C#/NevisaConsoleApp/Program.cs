using RestSharp;
using System.IO;
using System.Text.Json;
using System.Text.Json.Nodes;
using static Program;

class Program
{
    static void Login(string username, string password, out string token, out string api_key)
    {
        //Login

        var clientLogin = new RestClient("https://accounting.persianspeech.com/account/login");
        var requestLogin = new RestRequest();
        requestLogin.Method = Method.Post;
        requestLogin.RequestFormat = DataFormat.Json;
        requestLogin.AddHeader("Content-type", "application/json");
        var data = new
        {
            username_or_phone_or_email = username,
            password = password

        };
        requestLogin.AddJsonBody(data);

        var response = clientLogin.Execute(requestLogin);
        var loginData = System.Text.Json.JsonSerializer.Deserialize<JsonNode>(response.Content);

        token = loginData["user"]["token"].ToString();
        api_key = loginData["user"]["nevisa_service_account"]["current_service_record"]["key"].ToString();
    }

    static async Task<string> RecognizeFile(string auth_token, string api_key, string file_path)
    {
        HttpClient httpClient = new HttpClient();
        MultipartFormDataContent form = new MultipartFormDataContent();

        form.Add(new StringContent(auth_token), "auth_token");
        form.Add(new StringContent(api_key), "api_key");
        FileStream fs = File.OpenRead(file_path);
        form.Add(new StreamContent(fs), "file", Path.GetFileName(file_path));
        HttpResponseMessage response = await httpClient.PostAsync("https://api.persianspeech.com/recognize-file", form);

        response.EnsureSuccessStatusCode();
        httpClient.Dispose();
        string jsonString = response.Content.ReadAsStringAsync().Result;
        return jsonString;
    }

    static async Task<string> TaskProgress(string task_id, string progress_url)
    {
        HttpClient httpClient = new HttpClient();
        HttpResponseMessage response = await httpClient.GetAsync("https://api.persianspeech.com" + progress_url);
        response.EnsureSuccessStatusCode();
        httpClient.Dispose();
        string jsonString = response.Content.ReadAsStringAsync().Result;
        return jsonString;
    }


    static void Main()
    {
        MainAsync().Wait();
        // or, if you want to avoid exceptions being wrapped into AggregateException:
        //  MainAsync().GetAwaiter().GetResult();
    }

    static async Task MainAsync()
    {
        string token, api_key;

        Login("your username", "your password", out token, out api_key);

        Console.WriteLine("api_key:{0}\ntoken:{1}\n", api_key, token);

        var jsonString = await RecognizeFile(token, api_key, "C:\\test.wav");

        var recognizeFileResponse = JsonSerializer.Deserialize<JsonNode>(jsonString);

        Console.WriteLine("progress_url:{0}", recognizeFileResponse["progress_url"]);

        string state;

        JsonNode taskProgressResponse;

        do
        {
            var response = await TaskProgress((string)recognizeFileResponse["task_id"], (string)recognizeFileResponse["progress_url"]);
            taskProgressResponse = JsonSerializer.Deserialize<JsonNode>(response);

            Console.WriteLine("Progress : {0}%", taskProgressResponse["progress"]["percent"]);
            state = (string?)taskProgressResponse["state"];
            Thread.Sleep(1000);
        } while (state == "PROGRESS");
        Console.WriteLine("Final Result:{0}", taskProgressResponse["result"]["transcription"]["text"]);
    }
}