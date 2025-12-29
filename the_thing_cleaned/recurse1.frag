void main() {}
float cbar(int);
void cfoo(float)
{
	cbar(2);
}
void CB();
void CD();
void CA() { CB(); }
void CC() { CD(); }
void CBT();
void CDT();
void CAT() { CBT(); CBT(); CBT(); }
void CCT() { CDT(); CDT(); CBT(); }
void norA() {}
void norB() { norA(); }
void norC() { norA(); }
void norD() { norA(); }
void norE() { norB(); }
void norF() { norB(); }
void norG() { norE(); }
void norH() { norE(); }
void norI() { norE(); }
void norcA() { }
void norcB() { norcA(); }
void norcC() { norcB(); }
void norcD() { norcC(); norcB(); }
void norcE() { norcD(); }
