static main() {
auto ref, ea, fb, fe, name; 
ea = ScreenEA(); 
fb = GetFunctionAttr(ea, FUNCATTR_START); 
fe = GetFunctionAttr(ea, FUNCATTR_END); 
name = GetFunctionName(ea); 
Message("Function Name: %s\n", name); 
Message("Address Range: 0x%X - 0x%X\n", fb, fe); 
Message("Callers:\n"); 
ref = RfirstB(ea); 
while (ref != BADADDR) { 
auto caller_func = GetFunctionName(ref); 
if (caller_func != "") { 
auto caller_start = GetFunctionAttr(ref, FUNCATTR_START); 
Message("%s (0x%X)\n", caller_func, caller_start); } 
ref = RnextB(ea, ref); } }