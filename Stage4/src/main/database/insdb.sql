-- 1. Insert data into GymFacility
INSERT INTO GymFacility (location, phone, manager) VALUES
('Downtown Gym', '555-1234', 'John Doe'),
('Uptown Gym', '555-5678', 'Jane Smith'),
('Eastside Gym', '555-8765', 'Alice Johnson'),
('Westside Gym', '555-4321', 'Robert Brown'),
('Central Gym', '555-1357', 'Emily Davis');

-- 2. Insert data into Instructor
INSERT INTO Instructor (name, specialty, phone, email) VALUES
('Laura Thompson', 'Yoga', '555-1111', 'laura.thompson@example.com'),
('Mark Wilson', 'HIIT', '555-2222', 'mark.wilson@example.com'),
('Samantha Lee', 'Zumba', '555-3333', 'samantha.lee@example.com'),
('James Miller', 'Weights', '555-4444', 'james.miller@example.com'),
('Olivia Harris', 'Cardio', '555-5555', 'olivia.harris@example.com');

-- 3. Insert data into MembershipPlan
INSERT INTO MembershipPlan (planType, cost) VALUES
('Monthly', 50.00),
('Annual', 500.00),
('Monthly', 45.00),
('Annual', 480.00),
('Monthly', 55.00);

-- 4. Insert data into Member
INSERT INTO Member (name, email, phone, address, age, membershipStartDate, membershipEndDate) VALUES
('Michael Scott', 'michael.scott@example.com', '555-6666', '1725 Slough Avenue', 45, '2024-01-01', '2025-01-01'),
('Pam Beesly', 'pam.beesly@example.com', '555-7777', '123 Paper Street', 28, '2024-03-15', '2024-09-15'),
('Jim Halpert', 'jim.halpert@example.com', '555-8888', '456 Sale Lane', 30, '2024-02-10', '2025-02-10'),
('Dwight Schrute', 'dwight.schrute@example.com', '555-9999', '789 Beet Farm Road', 35, '2024-04-20', '2024-10-20'),
('Angela Martin', 'angela.martin@example.com', '555-0000', '101 Cat Lane', 32, '2024-01-20', '2025-01-20');

-- 5. Insert data into Class
INSERT INTO Class (className, classType, duration, classCapacity, instructorId, gymId) VALUES
('Morning Yoga', 'Yoga', 60, 20, 1, 1),
('HIIT Blast', 'HIIT', 45, 15, 2, 2),
('Zumba Fun', 'Zumba', 50, 25, 3, 3),
('Strength Training', 'Weights', 90, 10, 4, 4),
('Cardio Kick', 'HIIT', 60, 18, 5, 5);

-- 6. Insert data into Equipment
INSERT INTO Equipment (name, type, quantity, gymId) VALUES
('Treadmill', 'Cardio', 10, 1),
('Bench Press', 'Strength', 5, 2),
('Yoga Mats', 'Flexibility', 15, 3),
('Rowing Machine', 'Cardio', 6, 4),
('Foam Rollers', 'Recovery', 8, 5);

-- 7. Insert data into Payment
INSERT INTO Payment (memberId, planId, amountPaid, paymentDate) VALUES
(1, 2, 500.00, '2024-01-02'),
(2, 1, 50.00, '2024-03-15'),
(3, 2, 500.00, '2024-02-11'),
(4, 3, 45.00, '2024-04-21'),
(5, 5, 55.00, '2024-01-21');

-- 8. Insert data into Attends
INSERT INTO Attends (memberId, classId, attendanceDate) VALUES
(1, 1, '2024-05-01'),
(2, 3, '2024-05-02'),
(3, 2, '2024-05-03'),
(4, 4, '2024-05-04'),
(5, 5, '2024-05-05');
