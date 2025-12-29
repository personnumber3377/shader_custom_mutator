in vec4 bigColor;
in vec4 bigColor1_1;
in vec4 bigColor1_2;
in vec4 bigColor1_3;
in vec4 bigColor2;
in vec4 bigColor3;
in vec4 bigColor4;
in vec4 bigColor5;
in vec4 bigColor6;
in vec4 bigColor7;
in vec4 bigColor8;
in vec4 BaseColor;
in float d;
in float d2;
in float d3;
in float d4;
in float d5;
in float d6;
in float d7;
in float d8;
in float d9;
in float d10;
in float d11;
in float d12;
in float d14;
in float d15;
in float d16;
in float d17;
in float d18;
flat in int Count;
void main()
{
    vec4 color = BaseColor;
    while (true) {
        if (color.x < 0.33) {
            color += vec4(0.33);
            break;
        }
        if (color.x < 0.66) {
            color += vec4(0.66);
            break;
        }
        color += vec4(0.33);
        break;
    }
    while (color.x < d) {
        color += bigColor;
    }
    while (color.z < d) {
        color += bigColor1_1;
        if (color.w < d)
            continue;
        color += bigColor1_1;
    }
    while (color.x < 42.0) {
        ++color;
    }
    while (color.w < d2 && color.y < d3) {
        color += bigColor1_2;
    }
    while (color.z < d3) {
        color += bigColor1_3;
        if (color.y < d4)
            break;
        color += bigColor1_3;
    }
    for (int i = 0; i < Count; ++i) {
        color += bigColor2;
    }
    do {
        color += bigColor3;
    } while (color.x < d2);
    for (int i = 0; i < 42; ++i) {
        color.z += d3;
    }
    for (int i = 0; i < 100; ++i) {
        if (color.z < 20.0)
            color.x++;
        else
            color.y++;
        if (color.w < 20.0)
            if (color.z > color.y)
                0;
    }
    for (int i = 0; i < 120; ++i) {
        if (color.z < 20.0)
            color.x++;
        else
            color.y++;
    }
    for (int i = 0; i < 42; ++i) {
        color.z += d3;
        if (color.x < d4)
            continue;
        ++color.w;
    }
    for (int i = 0; i < 42; ++i) {
        color.z += d3;
        if (color.x < d4)
            break;
        ++color.w;
    }
    do {
        color += bigColor4;
        if (color.x < d4)
            continue;
        if (color.y < d4)
            color.y += d4;
        else
            color.x += d4;
    } while (color.z < d4);
    do {
        color += bigColor5;
        if (color.y < d5)
            color.y += d5;
    } while (color.x < d5);
    if (color.x < d6) {
        while (color.y < d6)
            color += bigColor6;
    } else {
        while (color.z < d6)
            color.z += bigColor6.z;
    }
    if (color.x < d6) {
        while (color.y < d6) {
            color += bigColor6;
            if (d7 < 1.0)
                break;
        }
    } else {
        while (color.z < d6)
            color.z += bigColor6.z;
    }
    do {
       if (d7 < 0.0)
           break;
       color += bigColor7;
       if (d7 < 1.0) {
           color.z++;
           break;
       }
       color += BaseColor;
    } while (true);
    do {
       if (d8 < 0.0)
           break;
       color += bigColor7;
       if (d8 < 1.0) {
           color.z++;
           if (d8 < 2.0) {
               color.y++;
           } else {
               color.x++;
           }
           break;
       }
       color += BaseColor;
    } while (color.z < d8);
    while (color.w < d9) {
        if (d9 > d8) {
            if (color.x <= d7) {
                if (color.z == 5.0)
                    color.w++;
                else
                    break;
            }
        }
    }
    while (color.z < d10) {
        color.y++;
        if (color.y < d11) {
            color.z++;
            if (color.w < d12)
                color.w++;
            else
                color.x++;
            continue;
        }
        color++;
        break;
    }
    while (color.x < 10.0) {
        color += bigColor8;
        if (color.z < d8)
            if (color.w < d6)
                continue;
        color.y += bigColor8.x;
    }
    color++;
    gl_FragColor = color;
    while (color.x < d14) {
        if (color.y < d15) {
            return;
        }
        else
            color++;
    }
    color++;
    while (color.w < d16) {
        color.w++;
    }
    while (color.w < d2 && color.y < d3) {
        color += bigColor1_2;
        if (color.z < d3)
            return;
    }
    do {
        if (color.y < d18)
            return;
        color++;
    } while (color.x < d17);
    while (color.y < d16) {
        if (color.w < d16) {
            discard;
        } else
            color++;
    }
    color++;
    gl_FragColor = color;
}
