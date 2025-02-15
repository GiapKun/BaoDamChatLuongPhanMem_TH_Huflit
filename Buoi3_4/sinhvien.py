class MonHoc:
    def __init__(self, ten_mon, diem=0):
        self.ten_mon = ten_mon
        self.diem = diem
        self.so_lan_thi_lai = 0

class SinhVien:
    def __init__(self, ma_sv="", ten_sv="", khoa_sv=""):
        self.sID = ma_sv
        self.hoTen = ten_sv
        self.khoa = khoa_sv
        self.ds_mon_hoc = []
        self.so_mon = 0

    def set_mon(self, mon):
        if not mon:
            return 0
        self.ds_mon_hoc.append(MonHoc(mon))
        self.so_mon += 1
        return 1

    def set_diem(self, mon, diem):
        for mon_hoc in self.ds_mon_hoc:
            if mon_hoc.ten_mon == mon:
                mon_hoc.diem = diem
                return 1
        return 0

    def tinh_dtb(self):
        if self.so_mon == 0:
            return 0
        tong_diem = sum(mon_hoc.diem for mon_hoc in self.ds_mon_hoc)
        return tong_diem / self.so_mon

    def tinh_diem_max(self):
        if self.so_mon == 0:
            return 0
        return max(mon_hoc.diem for mon_hoc in self.ds_mon_hoc)

    def ten_mon_max(self):
        diem_max = self.tinh_diem_max()
        return [mon_hoc.ten_mon for mon_hoc in self.ds_mon_hoc if mon_hoc.diem == diem_max]

    def ten_mon_thi_lai(self):
        return [mon_hoc.ten_mon for mon_hoc in self.ds_mon_hoc if mon_hoc.diem <= 4.5]

    def so_lan_thi_lai(self):
        result = {}
        for mon_hoc in self.ds_mon_hoc:
            if mon_hoc.diem <= 4.5:
                mon_hoc.so_lan_thi_lai += 1
                if mon_hoc.so_lan_thi_lai > 3:
                    mon_hoc.so_lan_thi_lai = 3  # Không được thi lại quá 3 lần
            result[mon_hoc.ten_mon] = mon_hoc.so_lan_thi_lai
        return result

    def check_chuyen_nganh(self):
        # Điều kiện 1: Tổng số môn đạt >= 5 từ 10 môn trở lên
        if self.so_mon < 10 or len([mon_hoc for mon_hoc in self.ds_mon_hoc if mon_hoc.diem >= 5]) < 5:
            return False

        # Điều kiện 2: Điểm trung bình 3 môn cơ sở >= 5
        mon_co_so = ["MonChuyenNganh", "ToanRoiRac", "TiengAnh"]
        diem_co_so = [mon_hoc.diem for mon_hoc in self.ds_mon_hoc if mon_hoc.ten_mon in mon_co_so]

        if len(diem_co_so) != 3 or sum(diem_co_so) / 3 < 5:
            return False

        return True

# Chương trình chính để test
if __name__ == "__main__":
    sv = SinhVien("SV001", "Nguyen Van A", "CNTT")

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

    sv.set_diem("MonChuyenNganh", 8)
    sv.set_diem("ToanRoiRac", 7)
    sv.set_diem("TiengAnh", 6)
    sv.set_diem("LapTrinhC", 5)
    sv.set_diem("LapTrinhJava", 4)
    sv.set_diem("CSDL", 3)
    sv.set_diem("ToanCaoCap", 9)
    sv.set_diem("VatLy", 2)
    sv.set_diem("TrietHoc", 7)
    sv.set_diem("KinhTe", 6)

    print(f"Điểm trung bình: {sv.tinh_dtb()}")
    print(f"Điểm cao nhất: {sv.tinh_diem_max()}")
    print(f"Môn học điểm cao nhất: {', '.join(sv.ten_mon_max())}")
    print(f"Môn học thi lại: {', '.join(sv.ten_mon_thi_lai())}")
    print(f"Số lần thi lại: {', '.join([f'{k}: {v}' for k, v in sv.so_lan_thi_lai().items()])}")
    print(f"Đủ điều kiện chọn chuyên ngành: {sv.check_chuyen_nganh()}")