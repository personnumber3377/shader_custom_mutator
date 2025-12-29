void main()
{
    hitObjectNV hObj;
    rayQueryEXT rq;
    vec3 pos;
    vec3 lss_pos[2];
    float rad;
    float lss_rad[2];
    float hitVal;
    bool isSphereHit, isLSSHit;
    pos = rayQueryGetIntersectionSpherePositionNV(rq, true);
    pos = rayQueryGetIntersectionSpherePositionNV(rq, false);
    rad = rayQueryGetIntersectionSphereRadiusNV(rq, true);
    rad = rayQueryGetIntersectionSphereRadiusNV(rq, false);
    rayQueryGetIntersectionLSSPositionsNV(rq, true, lss_pos);
    rayQueryGetIntersectionLSSPositionsNV(rq, false, lss_pos);
    rayQueryGetIntersectionLSSRadiiNV(rq, true, lss_rad);
    rayQueryGetIntersectionLSSRadiiNV(rq, false, lss_rad);
    hitVal = rayQueryGetIntersectionLSSHitValueNV(rq, true);
    hitVal = rayQueryGetIntersectionLSSHitValueNV(rq, false);
    isSphereHit = rayQueryIsSphereHitNV(rq, true);
    isSphereHit = rayQueryIsSphereHitNV(rq, false);
    isLSSHit = rayQueryIsLSSHitNV(rq, true);
    isLSSHit = rayQueryIsLSSHitNV(rq, false);
}
