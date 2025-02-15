import pytest
from sinhvien import SinhVien, MonHoc  # Assuming the code is in a file named `sinhvien.py`

# Test cases for SinhVien class
def test_set_mon():
    sv = SinhVien()
    assert sv.set_mon("Toan") == 1  # Successful addition
    assert sv.set_mon("") == 0  # Failed addition (empty string)
    assert sv.so_mon == 1  # Check if the number of subjects is updated

def test_set_diem():
    sv = SinhVien()
    sv.set_mon("Toan")
    assert sv.set_diem("Toan", 8.5) == 1  # Successful score update
    assert sv.set_diem("Ly", 7.0) == 0  # Failed score update (subject doesn't exist)

def test_tinh_dtb():
    sv = SinhVien()
    sv.set_mon("Toan")
    sv.set_mon("Ly")
    sv.set_diem("Toan", 8.0)
    sv.set_diem("Ly", 6.0)
    assert sv.tinh_dtb() == 7.0  # Average score calculation

def test_tinh_diem_max():
    sv = SinhVien()
    sv.set_mon("Toan")
    sv.set_mon("Ly")
    sv.set_diem("Toan", 8.0)
    sv.set_diem("Ly", 9.0)
    assert sv.tinh_diem_max() == 9.0  # Maximum score

def test_ten_mon_max():
    sv = SinhVien()
    sv.set_mon("Toan")
    sv.set_mon("Ly")
    sv.set_diem("Toan", 9.0)
    sv.set_diem("Ly", 9.0)
    assert "Toan" in sv.ten_mon_max()  # Both subjects have the highest score
    assert "Ly" in sv.ten_mon_max()

def test_ten_mon_thi_lai():
    sv = SinhVien()
    sv.set_mon("Toan")
    sv.set_mon("Ly")
    sv.set_diem("Toan", 4.0)
    sv.set_diem("Ly", 5.0)
    assert "Toan" in sv.ten_mon_thi_lai()  # Only "Toan" has a score <= 4.5
    assert "Ly" not in sv.ten_mon_thi_lai()

def test_so_lan_thi_lai():
    sv = SinhVien()
    sv.set_mon("Toan")
    sv.set_diem("Toan", 4.0)
    sv.so_lan_thi_lai()  # First retake
    sv.so_lan_thi_lai()  # Second retake
    sv.so_lan_thi_lai()  # Third retake
    sv.so_lan_thi_lai()  # Fourth retake (should not exceed 3)
    assert sv.so_lan_thi_lai()["Toan"] == 3  # Check retake count

def test_check_chuyen_nganh():
    sv = SinhVien()
    # Add 10 subjects
    sv.set_mon("MonChuyenNganh")
    sv.set_mon("ToanRoiRac")
    sv.set_mon("TiengAnh")
    sv.set_mon("LapTrinhC")
    sv.set_mon("LapTrinhJava")
    sv.set_mon("CSDL")
    sv.set_mon("ToanCaoCap")
    sv.set_mon("VatLy")
    sv.set_mon("TrietHoc")
    sv.set_mon("KinhTe")

    # Set scores for 5 subjects >= 5
    sv.set_diem("MonChuyenNganh", 8)
    sv.set_diem("ToanRoiRac", 7)
    sv.set_diem("TiengAnh", 6)
    sv.set_diem("LapTrinhC", 5)
    sv.set_diem("LapTrinhJava", 6)

    # Set scores for the remaining subjects
    sv.set_diem("CSDL", 4)
    sv.set_diem("ToanCaoCap", 3)
    sv.set_diem("VatLy", 2)
    sv.set_diem("TrietHoc", 7)
    sv.set_diem("KinhTe", 6)

    # Check if the student meets the specialization requirements
    assert sv.check_chuyen_nganh() == True  # Meets all conditions

    # Test failing condition (not enough subjects with score >= 5)
    sv.set_diem("LapTrinhC", 4)
    assert sv.check_chuyen_nganh() == True