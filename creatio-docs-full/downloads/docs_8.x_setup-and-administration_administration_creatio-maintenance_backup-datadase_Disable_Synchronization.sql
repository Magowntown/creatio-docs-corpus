DELETE FROM QRTZ_TRIGGERS;

IF EXISTS (SELECT * FROM syscolumns WHERE id = OBJECT_ID('MailboxSyncSettings') AND name = 'ExchangeAutoSyncActivity')
BEGIN
	declare @sql nvarchar(500);
	set @sql = 'UPDATE MailboxSyncSettings
		SET EnableMailSynhronization = 0,
			ExchangeAutoSynchronization = 0,
			ExchangeAutoSyncActivity = 0,
			UserName = '''',
			UserPassword = '''';
	';
	exec sp_executesql @sql;
END

IF EXISTS (SELECT 1 FROM SocialAccount)
BEGIN
	UPDATE ssv
		SET ssv.IntegerValue = 0
	FROM SysSettingsValue ssv
		INNER JOIN SysSettings ss 
			ON ssv.SysSettingsId = ss.Id
	WHERE ss.Code IN ('GoogleContactSynchInterval', 'GoogleCalendarSynchInterval');

	UPDATE SocialAccount
		SET "Login" = '',
			AccessToken = '';
END;


IF (EXISTS (SELECT
              *
       FROM INFORMATION_SCHEMA.TABLES
       WHERE TABLE_NAME = 'BulkEmail'
       AND TABLE_SCHEMA = 'dbo')
)
BEGIN
UPDATE BulkEmail
SET StatusId = 'A89E3500-3E51-4B68-B512-80ADF19738E7';
END;

IF (EXISTS (SELECT
              *
       FROM INFORMATION_SCHEMA.TABLES
       WHERE TABLE_NAME = 'Campaign'
       AND TABLE_SCHEMA = 'dbo')
)
BEGIN
UPDATE Campaign
SET CampaignStatusId = '5B792494-D40F-4B2B-8CFD-AB75AC5D33AA';
END


DECLARE @ReplacedSysSettingsValue TABLE
(
	[SysSettingsId] [uniqueidentifier] NOT NULL, 
	[Code] [nvarchar](50) NOT NULL,
	[TextValue] [nvarchar](max) NOT NULL,
	[BooleanValue] [bit] NOT NULL
)
INSERT INTO @ReplacedSysSettingsValue (SysSettingsId, Code, TextValue, BooleanValue)
	VALUES 
		-- mysite1
		('D4CED280-1251-4AD2-940E-049AE3BC1A9B', 'TmAMomentOfStillness', '', 1)
		,('451C8971-68F3-4544-BBBE-49D64A418152', 'TmDomen', N'https://mysite.creatio.com', '')
		-- mysite2
		,('8E3E5CD2-0EEB-4C2C-85BB-F72F0C114980', 'AipAllowSynchronization1C', '', 0)
		,('88328a78-3264-4640-92d3-ff9c40df2913', 'SiteBaseUrl', N'https://dev-mysite2.creatio.com', '');

DECLARE @ReplaceSettingsValueTemplate NVARCHAR(MAX) = 'UPDATE SysSettingsValue 
SET TextValue = @TextValue, BooleanValue = @BooleanValue
FROM SysSettingsValue v JOIN SysSettings s ON v.SysSettingsId = s.Id
WHERE s.Id = @SysSettingsId AND s.Code = @Code;';
DECLARE @Cmd nvarchar(MAX);
DECLARE @SysSettingsId uniqueidentifier
	,@Code [nvarchar](50)
	,@TextValue [nvarchar](max)
	,@BooleanValue bit;
DECLARE cur CURSOR FAST_FORWARD READ_ONLY LOCAL FOR
	SELECT SysSettingsId, Code, TextValue, BooleanValue FROM @ReplacedSysSettingsValue;
OPEN cur;
	
FETCH NEXT FROM cur INTO @SysSettingsId, @Code, @TextValue, @BooleanValue;
WHILE @@FETCH_STATUS = 0 BEGIN
	SET @Cmd = REPLACE(@ReplaceSettingsValueTemplate, '@TextValue', QUOTENAME(@TextValue, ''''));
	SET @Cmd = REPLACE(@Cmd, '@BooleanValue', @BooleanValue);
	SET @Cmd = REPLACE(@Cmd, '@SysSettingsId', QUOTENAME(@SysSettingsId, ''''));
	SET @Cmd = REPLACE(@Cmd, '@Code', QUOTENAME(@Code, ''''));
	PRINT @Cmd;
	EXEC (@Cmd);
	FETCH NEXT FROM cur INTO @SysSettingsId, @Code, @TextValue, @BooleanValue;
END
	
CLOSE cur;
DEALLOCATE cur;
