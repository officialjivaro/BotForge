using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows.Controls;

namespace BotForge
{
    public class Populate
    {
        private static string GetProxiesFilePath()
        {
            string username = Environment.UserName;
            return $@"C:\Users\{username}\Jivaro\BotForge\Data\Main\proxies.json";
        }

        public static void PopulateProxiesComboBox(ComboBox comboBox)
        {
            try
            {
                string filePath = GetProxiesFilePath();

                if (File.Exists(filePath))
                {
                    string json = File.ReadAllText(filePath);
                    List<SaveProxies.Proxy> proxies = JsonConvert.DeserializeObject<List<SaveProxies.Proxy>>(json) ?? new List<SaveProxies.Proxy>();

                    comboBox.ItemsSource = proxies.Select(p => p.ProxyIP).ToList();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error populating proxies: {ex.Message}");
            }
        }

        public static SaveProxies.Proxy GetProxyDetails(string proxyIP)
        {
            try
            {
                string filePath = GetProxiesFilePath();

                if (File.Exists(filePath))
                {
                    string json = File.ReadAllText(filePath);
                    List<SaveProxies.Proxy> proxies = JsonConvert.DeserializeObject<List<SaveProxies.Proxy>>(json) ?? new List<SaveProxies.Proxy>();

                    return proxies.FirstOrDefault(p => p.ProxyIP == proxyIP);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error retrieving proxy details: {ex.Message}");
            }

            return null;
        }
    }
}
