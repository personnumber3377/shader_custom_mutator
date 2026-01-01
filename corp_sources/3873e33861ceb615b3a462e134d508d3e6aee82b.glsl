#version 300 es
        uniform b
        {
            float f;
        } blockInstance;
        void main() {
            gl_Position = vec4(true ? 0.0 : blockInstance.f);
        }