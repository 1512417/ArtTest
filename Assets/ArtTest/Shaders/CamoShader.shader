Shader "Custom/CamoShader"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _WhiteColor ("White Areas Color", Color) = (1,1,1,1)
        _GreyColor ("Grey Areas Color", Color) = (0.5,0.5,0.5,1)
        _BlackColor ("Black Areas Color", Color) = (0,0,0,1)
        _WhiteThreshold ("White Threshold", Range(0,1)) = 0.3
        _GreyThreshold ("Grey Threshold", Range(0,1)) = 0.15
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            float4 _WhiteColor;
            float4 _GreyColor;
            float4 _BlackColor;
            float _WhiteThreshold;
            float _GreyThreshold;

            v2f vert (appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 col = tex2D(_MainTex, i.uv);
                float brightness = dot(col.rgb, float3(0.299, 0.587, 0.114)); // Convert to grayscale

                fixed4 finalColor;
                
                if (brightness > _WhiteThreshold)
                {
                    finalColor = _WhiteColor;
                }
                else if (brightness > _GreyThreshold)
                {
                    finalColor = _GreyColor;
                }
                else
                {
                    finalColor = _BlackColor;
                }

                return finalColor;
            }
            ENDCG
        }
    }
}