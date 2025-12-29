precision highp float;
precision mediump int;
layout(binding=0, set=0, input_attachment_index=0) tileImageEXT highp attachmentEXT in_color;
layout(location=0) out highp vec4 out_color;
void main(void)
{
     out_color = colorAttachmentReadEXT(in_color);
}
