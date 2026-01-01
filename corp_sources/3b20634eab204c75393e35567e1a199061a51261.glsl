#version 300 es
        precision mediump float;
        out vec4 out_fragColor;
        uniform bool u;
        void main()
        {
            int counter = 0;
            if (false)
            {
                while (u)
                {
                    if (++counter > 2)
                    {
                        break;
                    }
                }
            }
            out_fragColor = vec4(0.0);
        }