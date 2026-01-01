#version 300 es
        uniform b
        {
            float f;
        };
        void main() {
            gl_Position = vec4(true ? 0.0 : f);
        }