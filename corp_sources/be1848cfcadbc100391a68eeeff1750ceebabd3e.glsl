#version 300 es
        uniform struct
        {
            float field;
        } u;

        void main()
        {
            gl_Position = vec4(u.field, 0.0, 0.0, 1.0);
        }