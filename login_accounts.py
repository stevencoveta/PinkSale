import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level

async def main():
    api = API() 

    # ADD ACCOUNTS (for CLI usage see BELOW)
    await api.pool.add_account("meikio6l", "lhv2T77wb1exZj0C", "ploxexunyoow@outlook.com", "dgeXCMlS42l")
    await api.pool.add_account("girishibovn", "Cxy74vADDSFY1s5s", "staberobpoau@outlook.com", "m826lw7hONjt")
    await api.pool.add_account("innakisj", "nxaxq9KvVeiqA6PN", "eninsulsowh@outlook.com", "jvb82Vkif90SP")
    await api.pool.add_account("zaitonisq", "LeOiFA2n7BYq0W95", "asflordeiyz@outlook.com", "ZDnVhX49o5J")
    await api.pool.add_account("patsujiemy", "mVxjJ4ef39Wnq8Qb", "monslarustake@outlook.com", "liYyDBlODBs")
    await api.pool.add_account("mesuriwaoj", "zhb65DYByhql1uKS", "utulindzuhy@outlook.com", "m4FtVps8AulK")
    await api.pool.add_account("beraitsu31", "kbYaw5z0ERaHGZ06", "elvifansu3m@outlook.com", "4R8ftrBumuU")
    await api.pool.add_account("gorodepo0y", "jVdisqPKah19yqls", "uanephconno48@outlook.com", "Eahxo5XtDBsd")
    await api.pool.add_account("gotoyomi8v", "tgAAunJORkniYdXY", "nordlantuamemk@outlook.com", "7vIPEg4bC8")
    await api.pool.add_account("taikihik9", "YL1f6Amh4LYfvqp4", "lustficcilbig1@outlook.com", "YDwHjs61qFV3R")


    await api.pool.login_all()
if __name__ == "__main__":
    asyncio.run(main())