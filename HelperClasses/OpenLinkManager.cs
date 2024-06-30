using System.Diagnostics;

namespace BotForge
{
    public static class OpenLinkManager
    {
        public static void OpenLink(string url)
        {
            try
            {
                Process.Start(new ProcessStartInfo
                {
                    FileName = url,
                    UseShellExecute = true
                });
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error opening link: {ex.Message}");
            }
        }
    }
}
