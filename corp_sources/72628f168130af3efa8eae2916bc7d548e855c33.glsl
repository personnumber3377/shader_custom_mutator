#version 300 es
        precision mediump float;
        out vec4 out_fragColor;
        uniform int u;
        void main()
        {
            if (false)
            {
                switch (u)
                {
                    case 1:
                        out_fragColor = vec4(2.0);
                    default:
                        out_fragColor = vec4(1.0);
                }
            }
            out_fragColor = vec4(0.0);
        }