using UnityEngine;
using UnityEditor;
using System.IO;

[CreateAssetMenu(fileName = "CamoColors", menuName = "Camo/Color Settings")]
public class CamoColors : ScriptableObject
{
    public Color whiteColor = Color.white;
    public Color greyColor = Color.gray;
    public Color blackColor = Color.black;

    [ContextMenu("Import Colors From JSON")]
    public void ImportFromJson()
    {
        string path = EditorUtility.OpenFilePanel("Select JSON File", "", "json");
        if (string.IsNullOrEmpty(path)) return;

        string jsonContent = File.ReadAllText(path);
        JsonUtility.FromJsonOverwrite(jsonContent, this);
        EditorUtility.SetDirty(this);
        AssetDatabase.SaveAssets();
    }
}