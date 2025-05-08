using UnityEngine;
using UnityEditor;

public class CamoMaterialApplier : MonoBehaviour
{
    private Material targetMaterial;
    public CamoColors camoSet;

    void Start()
    {
        targetMaterial = GetComponent<MeshRenderer>().materials[0];
        ApplyColors();
    }


    public void ApplyColors()
    {
        if (targetMaterial == null || camoSet == null)
        {
            return;
        }
        
        targetMaterial.SetColor("_BlackColor", camoSet.blackColor);
        targetMaterial.SetColor("_GreyColor", camoSet.greyColor);
        targetMaterial.SetColor("_WhiteColor", camoSet.whiteColor);
    }
}