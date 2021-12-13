from core.employees.models import Employee
from core.accounts.models import Account
from core.blog_users.models import BlogUser
from common.enums import AccountRole, AccountGender
from utils.hash import Hash


async def feed_db():
    # create test administrator
    hash = Hash()
    if not await Account.exists(username='administrator'):
        account1 = await Account.create(username='administrator', email='administrator@example.com', 
                                password=hash.hash_password('administrator'), role=AccountRole.ADMINISTRATOR,
                                gender=AccountGender.MALE)
        await Employee.create(account=account1, firstname='Pan', lastname='Administrator', phone_number='600555400')

    # create test moderator
    if not await Account.exists(username='moderator'):
        account2 = await Account.create(username='moderator', email='moderator@example.com', 
                                password=hash.hash_password('moderator'), role=AccountRole.MODERATOR,
                                gender=AccountGender.MALE)
        await Employee.create(account=account2, firstname='Pan', lastname='Moderator', phone_number='601555400')
        await BlogUser.create(account=account2)

    # create test standard user
    if not await Account.exists(username='standard'):
        account3 = await Account.create(username='standard', email='standard@example.com', 
                                password=hash.hash_password('standard'), role=AccountRole.STANDARD,
                                gender=AccountGender.MALE)
        await BlogUser.create(account=account3)