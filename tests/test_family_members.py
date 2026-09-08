import unittest
from backend.family_members import FamilyMemberService

class FamilyMemberServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = FamilyMemberService()

    def test_add_and_list_member(self):
        member = self.service.add_member(
            user_id=1,
            name="父亲",
            relation="父亲",
            gender="男",
            birth_date="1968-05-20",
        )
        self.assertEqual(member["member_id"], 1)
        self.assertEqual(len(self.service.list_members(1)), 1)

    def test_duplicate_member_is_rejected(self):
        self.service.add_member(1, "张三", "父亲", "男", "1968-05-20")
        with self.assertRaises(ValueError):
            self.service.add_member(1, "张三", "父亲", "男", "1968-05-20")

    def test_user_cannot_modify_another_users_member(self):
        member = self.service.add_member(1, "李四", "母亲", "女", "1970-03-08")
        with self.assertRaises(KeyError):
            self.service.update_member(2, member["member_id"], name="非法修改")

if __name__ == "__main__":
    unittest.main()
