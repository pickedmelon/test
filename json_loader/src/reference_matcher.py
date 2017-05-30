import re
from nltk.tokenize import sent_tokenize
TOKEN = "[^,;]*"
NAME_TOKEN = "[A-Z&][^ ]*[,\.]? ?"
REF_TOKEN = "\(%s\)" % TOKEN
NAME_TOKENS = "(%s){1,6}" % NAME_TOKEN
CITATION_TOKEN = "[0-9]+ [^,]+ [0-9]+"
CITATION_TOKEN_EXTRA = CITATION_TOKEN + "(, [0-9]+)?"
CITATION_TOKENS = "(%s, ){0,6}%s" % (CITATION_TOKEN_EXTRA, CITATION_TOKEN_EXTRA)


ref_s1 = " ?".join([NAME_TOKENS, " v\. ", NAME_TOKENS, ",", CITATION_TOKENS, REF_TOKEN])
ref_s2 = " ?".join([NAME_TOKENS, " v\. ", NAME_TOKENS, ",", CITATION_TOKENS])
ref_s3 = " ?".join(["In re ", NAME_TOKENS, ",", CITATION_TOKENS, REF_TOKEN])

res1 = map(lambda s: re.compile(s), [ref_s1, ref_s2, ref_s3])


def bulk_match(res, s):
    result = set([])
    for reg in res:
        for m in reg.finditer(s):
            result.add(s[m.start(): m.end()])
    dedup = []
    for i in result:
        flag = False
        for j in result:
            if i !=j and i in j:
                flag = True
                break
        if not flag:
            dedup.append(i)
    return dedup


def find_reference(para):
    return bulk_match(res1, para)


def test():

    cases = [
        "Florow v. Louisville & Nashville Railroad Co., 502 F. Supp. 1 (M.D.Tenn.1979)",
        "Knoxville Traction Co. v. Lane, 103 Tenn. 376, 53 S.W. 557 (1899)",
        "Burlington N.R. Co. v. Oklahoma Tax Comm'n, 481 U.S. 454, 461, 107 S. Ct. 1855, 1859, 95 L. Ed. 2d 404 (1987)",
        "In re Demonica, 345 B.R. 895 (Bankr.N.D.Ill.2006)"
    ]
    sample = ". This is dummy. ".join(cases)
    results = find_reference(sample)
    # print results
    assert len(results) == len(cases), results
    for r in results:
        assert "dummy" not in r, r
        assert "This" not in r, r
        assert r in cases, r

test()