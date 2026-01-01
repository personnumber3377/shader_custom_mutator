#version 100
#extension GL_OES_standard_derivatives : require

    precision mediump float;
    varying float x;

    void main()
    {
        gl_FragColor = vec4(dFdy(x));
    }