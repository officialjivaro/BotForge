using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows;
using System.Xml;

namespace BotForge
{
    public class SaveProxies
    {
        private static string GetProxiesFilePath()
        {
            string username = Environment.UserName;
            return $@"C:\Users\{username}\Jivaro\BotForge\Data\Main\proxies.json";
        }

        public static void SaveProxy(string proxyIP, int port, string proxyType, bool requiresAuth, string username, string password)
        {
            try
            {
                string filePath = GetProxiesFilePath();

                List<Proxy> proxies = new List<Proxy>();

                if (File.Exists(filePath))
                {
                    string json = File.ReadAllText(filePath);
                    proxies = JsonConvert.DeserializeObject<List<Proxy>>(json) ?? new List<Proxy>();
                }

                Proxy existingProxy = proxies.FirstOrDefault(p => p.ProxyIP == proxyIP);

                if (existingProxy != null)
                {
                    existingProxy.Port = port;
                    existingProxy.ProxyType = proxyType;
                    existingProxy.RequiresAuth = requiresAuth;
                    existingProxy.Username = username;
                    existingProxy.Password = password;
                }
                else
                {
                    proxies.Add(new Proxy
                    {
                        ProxyIP = proxyIP,
                        Port = port,
                        ProxyType = proxyType,
                        RequiresAuth = requiresAuth,
                        Username = username,
                        Password = password
                    });
                }

                string updatedJson = JsonConvert.SerializeObject(proxies, Newtonsoft.Json.Formatting.Indented);
                File.WriteAllText(filePath, updatedJson);

                Console.WriteLine("Proxies successfully saved.");
                MessageBox.Show("Proxies successfully saved.", "Success", MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error saving proxies: {ex.Message}");
                MessageBox.Show($"Error saving proxies: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        public class Proxy
        {
            public string ProxyName { get; set; }
            public string ProxyIP { get; set; }
            public int Port { get; set; }
            public string ProxyType { get; set; }
            public bool RequiresAuth { get; set; }
            public string Username { get; set; }
            public string Password { get; set; }
        }
    }
}
