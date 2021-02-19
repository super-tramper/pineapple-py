CREATE OR REPLACE Procedure Test(testParam1 integer in, testParam2 integer out) IS
V_SQL char;
BEGIN

  V_SQL:='BEGIN OPEN :C_RES FOR SELECT * FROM DUAL; END;';

  EXECUTE IMMEDIATE V_SQL;

END SP_TEST;