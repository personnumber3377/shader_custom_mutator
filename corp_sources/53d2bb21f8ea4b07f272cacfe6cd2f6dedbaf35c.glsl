#version 300 es
        uniform b
        {
            float f[3];
        };
        void main() {
            if (f.length() > 1)
            {
                gl_Position = vec4(1.0);
            }
            else
            {
                gl_Position = vec4(0.0);
            }
        }