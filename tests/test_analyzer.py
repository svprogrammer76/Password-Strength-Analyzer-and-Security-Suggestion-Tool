import os, sys, tempfile, sqlite3
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),"..","backend")))
from services.password_analyzer import analyze_password
from services.pattern_detector import detect_sequences,detect_keyboard_patterns,detect_repetition
from services.password_generator import generate_password
from services.analytics import record
def test_empty(): assert analyze_password("")["score"]==0
def test_one_character(): assert analyze_password("x")["metrics"]["length"]==1
def test_short_number(): assert analyze_password("123")["classification"]=="VERY WEAK"
def test_common(): assert analyze_password("password")["metrics"]["common_password"]
def test_long_repeat_weak(): assert analyze_password("aaaaaaaaaaaaaaaa")["score"]<60
def test_lowercase(): assert not analyze_password("onlylowercase")["metrics"]["uppercase"]
def test_uppercase(): assert analyze_password("ONLYUPPERCASE")["metrics"]["uppercase"]
def test_numbers(): assert analyze_password("123456789")["metrics"]["digits"]
def test_symbols(): assert analyze_password("!@#$%^&*")["metrics"]["symbols"]
def test_mixed(): assert analyze_password("aZ7!rT9#kL2@")["metrics"]["character_type_count"]==4
def test_ascending_numeric(): assert "1234" in detect_sequences("ab1234xy")
def test_descending_numeric(): assert "9876" in detect_sequences("x9876y")
def test_ascending_letters(): assert "abcd" in detect_sequences("abcde")
def test_keyboard(): assert "qwerty" in detect_keyboard_patterns("qwerty2026!")
def test_repeat_chars(): assert "repeated_characters" in detect_repetition("AAAAAA123!")
def test_repeat_substring(): assert "repeated_substring" in detect_repetition("abcabcabc")
def test_word_number(): assert "predictable_structure" in [f["code"] for f in analyze_password("welcome123")["findings"]]
def test_year(): assert "year_pattern" in analyze_password("Cedar!2026")["metrics"]["structure_types"]
def test_name_context(): assert analyze_password("Rahul@123",{"name":"Rahul"})["metrics"]["personal_context_overlap"]
def test_birth_context(): assert analyze_password("Tree#1988",{"year":"1988"})["metrics"]["personal_context_overlap"]
def test_long_phrase(): assert analyze_password("copper lantern orbit meadow quiet harbor")["metrics"]["length"]>20
def test_unicode(): assert analyze_password("pássphräsé🌲")["metrics"]["length"]>0
def test_spaces(): assert analyze_password("blue river quiet meadow")["metrics"]["spaces"]
def test_max_length(): assert analyze_password("a"*1024)["metrics"]["length"]==1024
def test_reject_too_long():
    try: analyze_password("a"*1025)
    except ValueError: assert True
    else: assert False
def test_classification_valid(): assert analyze_password("sample")["classification"] in {"VERY WEAK","WEAK","MODERATE","STRONG","VERY STRONG"}
def test_suggestions_specific(): assert any("sequence" in x.lower() for x in analyze_password("123456")["suggestions"])
def test_generator_length(): assert len(generate_password(20))==20
def test_generator_character_groups(): assert generate_password(16,uppercase=False,lowercase=True,numbers=False,symbols=False).islower()
def test_metadata_has_no_password_column():
    p=tempfile.mktemp(suffix=".sqlite3"); record(analyze_password("synthetic demo only!"),p); db=sqlite3.connect(p)
    columns={row[1] for row in db.execute("pragma table_info(analyses)")}; db.close(); os.unlink(p)
    assert "password" not in columns and "password_hash" not in columns
def test_result_does_not_return_password(): assert "password" not in analyze_password("synthetic demo")
