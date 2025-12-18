PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL
);
INSERT INTO users VALUES('admin','W34therBC0ld!154!37!','Weather','Admin');
INSERT INTO users VALUES('ed','eY5+6hJ9wDhE+Le9vi9JVIf5YP4OAWR7HfbRi5tG','Ed','S');
INSERT INTO users VALUES('josh','YUCH+VOeVJzbt8qt5sPnYLssmz60rosUwS0LfRAR','Josh','W');
INSERT INTO users VALUES('lynn','c3roIHsci3X1Dh7B7hdXtpfJcBWiQrxWqq9LrxOK','Lynn','S');
INSERT INTO users VALUES('patrick','5kiKq4ebUWxxbhrEPji01QcV5kYUKin4zBSPiOcu','Patrick','C');
INSERT INTO users VALUES('paul','5Pvf20wfDVXcQ9jgv96Z6k7EoGm28M8BeK1PKcat','Paul','B');
INSERT INTO users VALUES('evan','4X07MTdPmk53RFFKBFZWyBovCnU6SkRDUNOLkWcE','Evan','B');
INSERT INTO users VALUES('thomas','DndrOnRSN4Kw0S/mSqD87G6GqUmmCZMHzfM09/KB','Thomas','B');
INSERT INTO users VALUES('chrisd','bT1sgRXrZEsIZytHMH7qhE51ieDPRwy+ML7Hnkc6','Chris','D');
INSERT INTO users VALUES('mark','qJxO+4BBySvqbpxfmNv0+dxJlAR1uXvgYXOkb4Ns','Mark','D');
INSERT INTO users VALUES('chrise','2useB6f9c14tlhqhrXOwSJj1FA2p5O7ywuHxpQL7','Chris','E');
INSERT INTO users VALUES('jared','Hdd0ngscc5XP6B8qvsWiDsPi6D31jd6tCZd6Nkn0','Jared','F');
INSERT INTO users VALUES('charlie','elrBun7XQdrj5nIXeZIVc+Ig11ESsTarl/tqlOBH','Charlie','G');
INSERT INTO users VALUES('tom','rdv/5wQAA55PkJY45emvhb0lk2fGx4nJL7h/qJqN','Tom','H');
INSERT INTO users VALUES('jj','aTYyYgbc3zSBPqJ7B2B2wQgyTRL4EpRw7Z0W6SqJ','Janusz','J');
INSERT INTO users VALUES('kevin','anaEQN2ptzRrv6sN06aoYs3Nu4YjpG4nEE+DGCnC','Kevin','M');
INSERT INTO users VALUES('torkel','fFZE44+eIcigZOoOuDwK7QqtBQNWhn/pp5tOE076','Torkel','O');
INSERT INTO users VALUES('kyle','GDFysqKvLRV4dkXBCfImxlPtF/AxB0igkVyA6l8W','Kyle','P');
INSERT INTO users VALUES('eric','OUQ1vSH7eZkZ/6UnImrMUqjK/FdFwzyfgqJrsxLM','Eric','P');
COMMIT;