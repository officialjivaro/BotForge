using System.Windows;

namespace BotForge
{
    public static class OpenWindowManager
    {
        public static void OpenWindow<T>() where T : Window, new()
        {
            T window = new T();
            window.ShowDialog();
        }
    }
}
