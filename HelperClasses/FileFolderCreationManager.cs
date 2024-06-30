using System;
using System.IO;

namespace BotForge
{
    public static class FileFolderCreationManager
    {
        public static void EnsureFileExists(string filePath)
        {
            try
            {
                string directoryPath = Path.GetDirectoryName(filePath);
                if (!Directory.Exists(directoryPath))
                {
                    Directory.CreateDirectory(directoryPath);
                }

                if (!File.Exists(filePath))
                {
                    File.Create(filePath).Dispose(); // Dispose immediately to release the file handle
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error ensuring file exists: {ex.Message}");
            }
        }

        public static void EnsureFolderExists(string folderPath)
        {
            try
            {
                if (!Directory.Exists(folderPath))
                {
                    Directory.CreateDirectory(folderPath);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error ensuring folder exists: {ex.Message}");
            }
        }
    }
}
