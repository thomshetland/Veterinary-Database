#
CREATE TRIGGER restrict_manager_count
BEFORE INSERT ON staff FOR EACH ROW
BEGIN
    DECLARE managersFound INT;

    IF NEW.position = 'MANAGER' THEN
        SELECT COUNT(*) INTO managersFound FROM staff WHERE position = 'MANAGER' and clinicID = NEW.clinicID;

        IF managersFound > 0 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Only one row can have the position MANAGER.';
        END IF;
    END IF;
END;