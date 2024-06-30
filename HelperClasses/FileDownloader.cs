using System;
using System.IO;
using System.Net;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;

public static class FileDownloader
{
    public static async Task DownloadFileAsync(string url, string destinationPath, ProgressBar progressBar)
    {
        try
        {
            string directory = Path.GetDirectoryName(destinationPath);
            if (!Directory.Exists(directory))
            {
                Directory.CreateDirectory(directory);
            }

            using (WebClient client = new WebClient())
            {
                client.Headers.Add("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36");

                client.DownloadProgressChanged += (s, e) =>
                {
                    Application.Current.Dispatcher.Invoke(() =>
                    {
                        progressBar.Value = e.ProgressPercentage;
                    });
                };

                client.DownloadFileCompleted += (s, e) =>
                {
                    if (e.Error != null)
                    {
                        MessageBox.Show($"Error downloading file: {e.Error.Message}");
                    }
                };

                await client.DownloadFileTaskAsync(new Uri(url), destinationPath);
            }
        }
        catch (IOException ioEx)
        {
            MessageBox.Show($"File is in use: {ioEx.Message}");
        }
        catch (Exception ex)
        {
            MessageBox.Show($"Error: {ex.Message}");
        }
    }
}
