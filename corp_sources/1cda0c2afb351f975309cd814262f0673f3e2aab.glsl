#version 300 es
        struct sType
        {
            float field;
        };
        uniform sType u;

        void main()
        {
            gl_Position = vec4(u.field, 0.0, 0.0, 1.0);
        }