#version 150

uniform sampler2DRect tex0;
uniform float brightness, contrast, saturation;

in vec2 texCoordVarying;
out vec4 outputColor;

void main() {
    vec2 coord = texCoordVarying;

    vec3 color = texture(tex0, coord).rgb;

    //brcosa
    const vec3 LumCoeff = vec3(0.2125, 0.7154, 0.0721);
    vec3 AvgLumin = vec3(0.5, 0.5, 0.5);
    vec3 intensity2 = vec3(dot(color, LumCoeff));
    vec3 satColor = mix(intensity2, color, saturation);
    vec3 conColor = mix(AvgLumin, satColor, contrast);
    
    //output
    outputColor = vec4(brightness * conColor, 1.0);
}
