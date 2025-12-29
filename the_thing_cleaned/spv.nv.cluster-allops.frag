layout(binding = 1) uniform accelerationStructureEXT as;
void main()
{
	rayQueryEXT rq;
	int id_candidate = rayQueryGetIntersectionClusterIdNV(rq, false);
	int id_committed = rayQueryGetIntersectionClusterIdNV(rq, true);
	bool test  = (id_candidate == gl_ClusterIDNoneNV) && (id_committed == gl_ClusterIDNoneNV);
}
