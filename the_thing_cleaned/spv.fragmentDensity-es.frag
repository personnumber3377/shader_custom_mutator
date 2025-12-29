layout (location = 0) out highp ivec2 FragSize;
layout (location = 2) out highp int FragInvocationCount;
void main () {
    FragSize = gl_FragSizeEXT;
    FragInvocationCount = gl_FragInvocationCountEXT;
}
