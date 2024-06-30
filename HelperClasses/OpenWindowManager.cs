using System.Windows;

namespace Jivaro_OSRS_Bot_Manager
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
