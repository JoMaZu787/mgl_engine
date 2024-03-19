#version 430 core
#define PI 3.1415926535897932384626433832795

layout (location=0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

struct Light {
    vec3 position;
    vec3 intensity;
};

uniform Light light;
uniform sampler2D u_texture_0;
uniform vec3 camPos;

vec3 getLight(vec3 albedo) {
    vec3 N = normalize(normal);
    vec3 V = normalize(camPos - fragPos);
    vec3 L = normalize(light.position - fragPos);

    // Calculate the half vector (microfacet normal)
    vec3 H = normalize(V + L);

    // Calculate the roughness (example value)
    float roughness = 1.0;

    // Calculate the NdotL and NdotV terms
    float NdotL = max(dot(N, L), 0.0);
    float NdotV = max(dot(N, V), 0.0);

    // Calculate the distribution term using GGX
    float alpha = roughness * roughness;
    float alpha2 = alpha * alpha;
    float NdotH = max(dot(N, H), 0.0);
    float D = alpha2 / (PI * pow(NdotH * NdotH * (alpha2 - 1.0) + 1.0, 2.0));

    // Calculate the geometric attenuation term
    float Vis = min(1.0, min(2.0 * NdotH * NdotV / dot(V, H), 2.0 * NdotH * NdotL / dot(V, H)));

    // Apply the intensity for specular
    vec3 intensity = light.intensity;

    // Calculate the specular term
    vec3 specular = (D * Vis * intensity) / (4.0 * NdotL * NdotV) * albedo;

    // Diffuse
    vec3 diffuse = (NdotL * intensity) * albedo;

    vec3 ambient = 0.1 * albedo;

    // Combine specular and diffuse reflections
    vec3 lighting = specular + diffuse + ambient;

    return lighting;
}

void main() {
    vec3 color = texture(u_texture_0, uv_0).rgb;
    fragColor = vec4(getLight(color), 1.0);
}
