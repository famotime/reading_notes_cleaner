"""随机抽取markdown笔记文件，并从中随机挑选句子，发送到邮件"""
import pathlib
import random
import json
import time
import yagmail


def select_random_notes(notes_path, select_file_num=5, select_note_num=1):
    md_files = notes_path.glob('*.md')
    selected_files = random.sample(list(md_files), select_file_num)
    selected_notes = []

    for selected_file in selected_files:
        with open(selected_file, encoding='utf-8') as f:
            lines = [line + f"-- 《{str(selected_file.stem).strip('《》').replace(' 》的笔记', '')}》\n" for line in f.readlines() if len(line) > 25 and not line.startswith('#')]
            selected_lines = random.sample(lines, select_note_num)
            selected_notes += (selected_lines)

    content = '\n'.join(selected_notes)
    return content


def read_mail_account(account_path, mailhost):
    """从json文件读取邮箱帐号信息，mailhost可取['189', '163', '139', 'qq']之一"""
    with open(account_path) as f:
        mail_accounts = json.load(f)
    mail_account = mail_accounts[mailhost]
    return mail_account['host'], mail_account['user'], mail_account['password']


if __name__ == "__main__":
    notes_path = pathlib.Path(r'C:\QMDownload\Backup\Wiz Knowledge\exported_md\读书摘录')
    content = select_random_notes(notes_path, select_file_num=5, select_note_num=2)
    print(content)

    account_path = pathlib.Path.cwd().parent / 'account/mail_accounts.json'    # 邮箱帐号信息保存路径
    mailhost = '189'    # mailhost可取['189', '163', '139', 'qq']之一
    mailreceiver = '672654917@qq.com'

    mailhost, mailuser, mailpassword = read_mail_account(account_path, mailhost)
    date = time.strftime("%Y%m%d", time.localtime())
    yag_server = yagmail.SMTP(user=mailuser, password=mailpassword, host=mailhost)
    yag_server.send(to=mailreceiver, subject=f'今日金句{date}', contents=[content])
    print(f'《今日金句{date}》邮件已发送。')
    yag_server.close()
