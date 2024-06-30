using BotForge;
using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;

namespace BotForge
{
    public partial class MainWindow : Window
    {
        private readonly CancellationTokenSource _cancellationTokenSource = new CancellationTokenSource();

        public MainWindow()
        {
            InitializeComponent();
            StartBackgroundWorker();
            Populate.PopulateProxiesComboBox(cmbProxies);
        }

        private async void DownloadOSBot_Click(object sender, RoutedEventArgs e)
        {
            string username = Environment.UserName;
            string basePath = $@"C:\Users\{username}\Jivaro\BotForge\Data\Clients\";
            DownloadProgressBar.Visibility = Visibility.Visible;
            await FileDownloader.DownloadFileAsync("https://osbot.org/mvc/get", Path.Combine(basePath, "OSBot.jar"), DownloadProgressBar);
            DownloadProgressBar.Visibility = Visibility.Collapsed;
        }

        private async void DownloadDreamBot_Click(object sender, RoutedEventArgs e)
        {
            string username = Environment.UserName;
            string basePath = $@"C:\Users\{username}\Jivaro\BotForge\Data\Clients\";
            DownloadProgressBar.Visibility = Visibility.Visible;
            await FileDownloader.DownloadFileAsync("https://dreambot.org/DBLauncher.jar", Path.Combine(basePath, "DreamBot.jar"), DownloadProgressBar);
            DownloadProgressBar.Visibility = Visibility.Collapsed;
        }

        private async void DownloadTRiBot_Click(object sender, RoutedEventArgs e)
        {
            string username = Environment.UserName;
            string basePath = $@"C:\Users\{username}\Jivaro\BotForge\Data\Clients\";
            DownloadProgressBar.Visibility = Visibility.Visible;
            await FileDownloader.DownloadFileAsync("https://installers.tribot.org/tribot-splash.jar", Path.Combine(basePath, "TRiBot.jar"), DownloadProgressBar);
            DownloadProgressBar.Visibility = Visibility.Collapsed;
        }

        private void SaveProxy_Click(object sender, RoutedEventArgs e)
        {
            string proxyIP = txtProxyIP.Text;
            int port = int.Parse(txtPort.Text);
            string proxyType = ((ComboBoxItem)cmbProxyType.SelectedItem).Content.ToString();
            bool requiresAuth = chkRequiresAuth.IsChecked ?? false;
            string username = txtUsername.Text;
            string password = txtPassword.Text;

            SaveProxies.SaveProxy(proxyIP, port, proxyType, requiresAuth, username, password);
            Populate.PopulateProxiesComboBox(cmbProxies);
        }

        private void cmbProxies_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (cmbProxies.SelectedItem != null)
            {
                string selectedProxyIP = cmbProxies.SelectedItem.ToString();
                var proxy = Populate.GetProxyDetails(selectedProxyIP);

                if (proxy != null)
                {
                    txtProxyIP.Text = proxy.ProxyIP;
                    txtPort.Text = proxy.Port.ToString();
                    cmbProxyType.SelectedItem = proxy.ProxyType;
                    chkRequiresAuth.IsChecked = proxy.RequiresAuth;
                    txtUsername.Text = proxy.Username;
                    txtPassword.Text = proxy.Password;
                }
            }
        }

        private void VisitBuyScriptFactory_Click(object sender, RoutedEventArgs e)
        {
            OpenLinkManager.OpenLink("https://www.osbot.org/forum/store/product/778-script-factory-20/");
        }

        private void VisitSettupGuide_Click(object sender, RoutedEventArgs e)
        {
            OpenLinkManager.OpenLink("https://www.jivarostore.com/product-information/user-guide/user-guide-jivaros-osbot-script-factory-scripts");
        }

        private void VisitWebsite_Click(object sender, RoutedEventArgs e)
        {
            OpenLinkManager.OpenLink("https://www.jivaro.net/");
        }

        private void VisitBuyJivaroScripts_Click(object sender, RoutedEventArgs e)
        {
            OpenLinkManager.OpenLink("https://www.jivarostore.com/product-information/jivaro-old-school-runescape-botting-scripts");
        }

        private void VisitBottingGuide_Click(object sender, RoutedEventArgs e)
        {
            OpenLinkManager.OpenLink("https://www.jivaro.net/content/guides/the-ultimate-guide-to-botting-old-school-runescape");
        }

        private void VisitCreateJagexAccount_Click(object sender, RoutedEventArgs e)
        {
            OpenLinkManager.OpenLink("https://account.jagex.com/en-GB/login/registration-start");
        }

        private void VisitDiscord_Click(object sender, RoutedEventArgs e)
        {
            OpenLinkManager.OpenLink("https://discord.gg/GDfX5BFGye");
        }

        private void VisitBuyProxies_Click(object sender, RoutedEventArgs e)
        {
            OpenLinkManager.OpenLink("https://www.jivaro.net/content/blog/the-best-affordable-proxy-providers");
        }

        private void StartBackgroundWorker()
        {
            var token = _cancellationTokenSource.Token;

            Task.Run(async () =>
            {
                while (!token.IsCancellationRequested)
                {
                    CheckFilesAndFolders();
                    await Task.Delay(TimeSpan.FromSeconds(30), token);
                }
            }, token);
        }

        private void CheckFilesAndFolders()
        {
            string username = Environment.UserName;
            string basePath = $@"C:\Users\{username}\Jivaro\BotForge\Data\Main\";

            FileFolderCreationManager.EnsureFileExists(System.IO.Path.Combine(basePath, "accounts.json"));
            FileFolderCreationManager.EnsureFileExists(System.IO.Path.Combine(basePath, "proxies.json"));
            FileFolderCreationManager.EnsureFileExists(System.IO.Path.Combine(basePath, "local_scripts.json"));

            FileFolderCreationManager.EnsureFolderExists($@"C:\Users\{username}\OSBot\Data\ProjectPact\OSRS Script Factory\Private Scripts\");
            FileFolderCreationManager.EnsureFolderExists($@"C:\Users\{username}\OSBot\Data\ProjectPact\OSRS Script Factory\Profiles\");
            FileFolderCreationManager.EnsureFolderExists($@"C:\Users\{username}\Jivaro\BotForge\Temp\");
            FileFolderCreationManager.EnsureFolderExists($@"C:\Users\{username}\Jivaro\BotForge\Sessions\");
            FileFolderCreationManager.EnsureFolderExists($@"C:\Users\{username}\Jivaro\BotForge\Data\Clients\");
            FileFolderCreationManager.EnsureFolderExists($@"C:\Users\{username}\Jivaro\BotForge\Data\Java\");
        }

        protected override void OnClosed(EventArgs e)
        {
            _cancellationTokenSource?.Cancel();
            base.OnClosed(e);
        }
    }
}
