-- User tablosundan bir user silinince;
-- -> user_page_info
-- -> ad_detailed_page
-- -> offer
-- -> favorites
-- -> compare
-- tablolarından o user ile ilişkilendirilmiş satırlar silinir.
-- Ancak reports ve blacklist tablolarından kullanıcı silinmez.

-- (Kullanıcılar banlanınca user tablosundan kullanıcı silinir. Banlanan kullanıcıların maili blacklist tablosunda tutulur[Bir daha kaydolamamaları için].) 

-- Ad_page tablosundan bir ad silinirse;
-- -> Favorites
-- -> Compare
-- -> Photos
-- -> Ad_utilities
-- tablolarından o ad ile ilişkilendirilmiş satırlar silinir.


CREATE TABLE Users (
	userID					INT				GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
	e_mail					VARCHAR(50)		NOT NULL UNIQUE CHECK (e_mail LIKE '%@itu.edu.tr'),
	hashed_password				VARCHAR(100)	NOT NULL,
	is_confirmed				BOOLEAN		DEFAULT FALSE,
    role                        BOOLEAN     DEFAULT FALSE
);

CREATE TABLE Department (
    departmentID 			INT 			GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    department_name 		VARCHAR(150) 	NOT NULL
);

CREATE TABLE User_page_info (
	userID_FK				INT				PRIMARY KEY,
	departmentID_FK 		INT,
    full_name 				VARCHAR(50)		NOT NULL,
    date_of_birth 			DATE,
    gender 					BOOLEAN,
    smoking 				BOOLEAN,
    pet 					BOOLEAN,
    ppURL 					TEXT,
    about 					VARCHAR(300),
    contact 				VARCHAR(100),
    RH 						BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (userID_FK) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (departmentID_FK) REFERENCES Department(departmentID)
);

CREATE TABLE District (
    districtID 				INT 			GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    district_name 			VARCHAR(30) 	UNIQUE NOT NULL
);

CREATE TABLE Neighborhood (
    neighborhoodID 			INT 			GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    neighborhood_name 		VARCHAR(40) 	NOT NULL,
	districtID_FK       	INT 			NOT NULL,
    FOREIGN KEY (districtID_FK) REFERENCES District(districtID)
);



CREATE TABLE Numberofroom (
    n_roomID 				INT 			GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    n_room 					VARCHAR(3) 		NOT NULL
);

CREATE TABLE Ad_page (
    adpageID 				INT 			GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    userID_FK 				INT,
    neighborhoodID_FK 		INT,
    n_roomID_FK 			INT,
    title 					VARCHAR(100) 	NOT NULL,
    price 					INT 			NOT NULL,
    adtype 					BOOLEAN,
    m2 						INT,
    n_floor 				INT,
    floornumber 			INT,
    pet 					BOOLEAN,
    smoking 				BOOLEAN,
    furnished 				BOOLEAN,
    description 			VARCHAR(300),
    address 				VARCHAR(300),
    gender_choices 			INT,
    ad_date 				TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userID_FK) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (neighborhoodID_FK) REFERENCES Neighborhood(neighborhoodID),
    FOREIGN KEY (n_roomID_FK) REFERENCES Numberofroom(n_roomID)
);

CREATE TABLE Offers (
    offerID 				INT 			GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    offererID_FK 			INT,
    offereeID_FK 			INT,
    send_message 			VARCHAR(150),
    FOREIGN KEY (offererID_FK) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (offereeID_FK) REFERENCES Users(userID) ON DELETE CASCADE
);

CREATE TABLE Favorites (
    userID_FK 				INT,
    adpageID_FK 			INT,
    PRIMARY KEY (userID_FK, adpageID_FK),
    FOREIGN KEY (userID_FK) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (adpageID_FK) REFERENCES Ad_page(adpageID) ON DELETE CASCADE
);

CREATE TABLE Compare (
    userID_FK 				INT,
    cmp1			 		INT,
    cmp2			 		INT,
    PRIMARY KEY (userID_FK, cmp1, cmp2),
    FOREIGN KEY (userID_FK) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (cmp1) REFERENCES Ad_page(adpageID) ON DELETE CASCADE,
    FOREIGN KEY (cmp2) REFERENCES Ad_page(adpageID) ON DELETE CASCADE
);

CREATE TABLE Photos (
    photoID 				INT 			GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    adpageID_FK 			INT,
    photoURL 				TEXT 			NOT NULL,
    FOREIGN KEY (adpageID_FK) REFERENCES Ad_page(adpageID) ON DELETE CASCADE
);

CREATE TABLE Reports (
    reportID 				INT 			GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    reporter 				INT,
    reportee	 			INT,
    description 			VARCHAR(140),
    report_date 			DATE,
    FOREIGN KEY (reporter) REFERENCES Users(userID),
    FOREIGN KEY (reportee) REFERENCES Users(userID) 
);

CREATE TABLE Blacklist (
    e_mail 				VARCHAR(50) 			PRIMARY KEY,
    ban_date 				TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ban_reason 				VARCHAR(150)
);


CREATE TABLE Utilities (
    utilityID 				INT 			GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    utility_name 			VARCHAR(50)
);

CREATE TABLE Ad_utilities (
    utilityID_FK 			INT,
    adpageID_FK 			INT,
    PRIMARY KEY (utilityID_FK, adpageID_FK),
    FOREIGN KEY (utilityID_FK) REFERENCES Utilities(utilityID),
    FOREIGN KEY (adpageID_FK) REFERENCES Ad_page(adpageID) ON DELETE CASCADE
);