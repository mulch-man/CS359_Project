-- 1. Attends Table
-- This table tracks the attendance of members in different classes.
-- The PRIMARY KEY ensures a member cannot have duplicate attendance records for the same class on the same date.
-- FOREIGN KEYS enforce relationships with the Class and Member tables.
CREATE TABLE "Attends" (
    "memberId" INTEGER,
    "classId" INTEGER,
    "attendanceDate" TEXT,
    PRIMARY KEY("memberId", "classId", "attendanceDate"),
    FOREIGN KEY("classId") REFERENCES "Class"("classId"),
    FOREIGN KEY("memberId") REFERENCES "Member"("memberId")
);

-- 2. Class Table
-- Stores information about fitness classes offered at the gym.
-- classType is restricted to specific valid values using a CHECK constraint.
-- FOREIGN KEYS link to Instructor and GymFacility tables.
CREATE TABLE Class (
    classId INTEGER PRIMARY KEY AUTOINCREMENT,
    className VARCHAR(50),
    classType VARCHAR(20) CHECK (classType IN ('Yoga', 'Zumba', 'HIIT', 'Weights')),
    duration NUMERIC NOT NULL, -- Duration in minutes, cannot be null
    classCapacity INTEGER NOT NULL, -- Max capacity, cannot be null
    instructorId INTEGER REFERENCES Instructor(instructorId),
    gymId INTEGER REFERENCES GymFacility(gymId)
);

-- 3. Equipment Table
-- Represents gym equipment available at each facility.
-- The 'type' column is limited to predefined categories using a CHECK constraint.
CREATE TABLE Equipment (
    equipmentId INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL, -- Equipment name cannot be null
    type VARCHAR(30) CHECK (type IN ('Cardio', 'Strength', 'Flexibility', 'Recovery')),
    quantity INTEGER(30), -- Quantity available
    gymId INTEGER REFERENCES GymFacility(gymId) -- Linked to a gym facility
);

-- 4. GymFacility Table
-- Details about each gym facility, including location and manager.
CREATE TABLE "GymFacility" (
    "gymId" INTEGER PRIMARY KEY AUTOINCREMENT,
    "location" VARCHAR(100) NOT NULL, -- Must have a location
    "phone" VARCHAR(50),
    "manager" VARCHAR(50)
);

-- 5. Instructor Table
-- Information about gym instructors, including specialties and contact details.
CREATE TABLE "Instructor" (
    "instructorId" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" VARCHAR(50),
    "specialty" VARCHAR(50),
    "phone" VARCHAR(15) NOT NULL, -- Phone number required
    "email" VARCHAR(100) NOT NULL -- Email required
);

-- 6. Member Table
-- Holds member details, including membership dates and contact information.
-- age must be at least 15, and membershipEndDate must be after membershipStartDate.
CREATE TABLE Member (
    memberId INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50),
    email VARCHAR(50) NOT NULL, -- Email cannot be null
    phone VARCHAR(15),
    address VARCHAR(100),
    age INTEGER CHECK (age >= 15),
    membershipStartDate TEXT NOT NULL, -- Start date required
    membershipEndDate TEXT NOT NULL CHECK (timediff(membershipEndDate, membershipStartDate) > 0) -- End date after start date
);

-- 7. MembershipPlan Table
-- Defines available membership plans with type and cost.
CREATE TABLE MembershipPlan (
    planId INTEGER PRIMARY KEY AUTOINCREMENT,
    planType VARCHAR(20) CHECK (planType IN ('Monthly', 'Annual')),
    cost NUMERIC NOT NULL -- Cost required
);

-- 8. Payment Table
-- Tracks payments made by members for their membership plans.
CREATE TABLE Payment (
    paymentId INTEGER PRIMARY KEY AUTOINCREMENT,
    memberId INTEGER REFERENCES Member(memberId),
    planId INTEGER REFERENCES MembershipPlan(planId),
    amountPaid REAL, -- Amount paid
    paymentDate TEXT NOT NULL -- Payment date required
);

-- 9. sqlite_sequence Table
-- Used internally by SQLite to track AUTOINCREMENT values.
CREATE TABLE sqlite_sequence(name, seq);
