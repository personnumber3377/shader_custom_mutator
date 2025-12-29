flat in int iInput;
out int bOut;
void main(){
    bool bTemp = false;
    bTemp  = bTemp || subgroupQuadAll(iInput > 0);
    bTemp  = bTemp || subgroupQuadAny(iInput > 0);
    bOut = bTemp == true ? 1 : 0;
}
