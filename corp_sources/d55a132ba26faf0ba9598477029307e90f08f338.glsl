void foo()
        {
        }
        varying vec4 v_varying;
        invariant v_varying;
        void main()
        {
           foo();
           gl_Position = v_varying;
        }