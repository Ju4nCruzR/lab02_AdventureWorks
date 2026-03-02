-- AdventureWorks OLTP Schema for PostgreSQL
-- Generated from SQL Server 2025

CREATE SCHEMA IF NOT EXISTS person;
CREATE SCHEMA IF NOT EXISTS sales;
CREATE SCHEMA IF NOT EXISTS purchasing;
CREATE SCHEMA IF NOT EXISTS dbo;
CREATE SCHEMA IF NOT EXISTS humanresources;
CREATE SCHEMA IF NOT EXISTS production;

CREATE TABLE IF NOT EXISTS dbo.awbuildversion (
    "systeminformationid" SMALLINT NOT NULL,
    "database version" VARCHAR(25) NOT NULL,
    "versiondate" TIMESTAMP NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS dbo.databaselog (
    "databaselogid" INTEGER NOT NULL,
    "posttime" TIMESTAMP NOT NULL,
    "databaseuser" VARCHAR(128) NOT NULL,
    "event" VARCHAR(128) NOT NULL,
    "schema" VARCHAR(128) NULL,
    "object" VARCHAR(128) NULL,
    "tsql" TEXT NOT NULL,
    "xmlevent" XML NOT NULL
);

CREATE TABLE IF NOT EXISTS dbo.errorlog (
    "errorlogid" INTEGER NOT NULL,
    "errortime" TIMESTAMP NOT NULL,
    "username" VARCHAR(128) NOT NULL,
    "errornumber" INTEGER NOT NULL,
    "errorseverity" INTEGER NULL,
    "errorstate" INTEGER NULL,
    "errorprocedure" VARCHAR(126) NULL,
    "errorline" INTEGER NULL,
    "errormessage" VARCHAR(4000) NOT NULL
);

CREATE TABLE IF NOT EXISTS humanresources.department (
    "departmentid" SMALLINT NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "groupname" VARCHAR(50) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS humanresources.employee (
    "businessentityid" INTEGER NOT NULL,
    "nationalidnumber" VARCHAR(15) NOT NULL,
    "loginid" VARCHAR(256) NOT NULL,
    "organizationnode" VARCHAR(100) NULL,
    "organizationlevel" SMALLINT NULL,
    "jobtitle" VARCHAR(50) NOT NULL,
    "birthdate" DATE NOT NULL,
    "maritalstatus" CHAR(1) NOT NULL,
    "gender" CHAR(1) NOT NULL,
    "hiredate" DATE NOT NULL,
    "salariedflag" BOOLEAN NOT NULL,
    "vacationhours" SMALLINT NOT NULL,
    "sickleavehours" SMALLINT NOT NULL,
    "currentflag" BOOLEAN NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS humanresources.employeedepartmenthistory (
    "businessentityid" INTEGER NOT NULL,
    "departmentid" SMALLINT NOT NULL,
    "shiftid" SMALLINT NOT NULL,
    "startdate" DATE NOT NULL,
    "enddate" DATE NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS humanresources.employeepayhistory (
    "businessentityid" INTEGER NOT NULL,
    "ratechangedate" TIMESTAMP NOT NULL,
    "rate" NUMERIC(19,4) NOT NULL,
    "payfrequency" SMALLINT NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS humanresources.jobcandidate (
    "jobcandidateid" INTEGER NOT NULL,
    "businessentityid" INTEGER NULL,
    "resume" XML NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS humanresources.shift (
    "shiftid" SMALLINT NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "starttime" TIME NOT NULL,
    "endtime" TIME NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS person.address (
    "addressid" INTEGER NOT NULL,
    "addressline1" VARCHAR(60) NOT NULL,
    "addressline2" VARCHAR(60) NULL,
    "city" VARCHAR(30) NOT NULL,
    "stateprovinceid" INTEGER NOT NULL,
    "postalcode" VARCHAR(15) NOT NULL,
    "spatiallocation" TEXT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS person.addresstype (
    "addresstypeid" INTEGER NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS person.businessentity (
    "businessentityid" INTEGER NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS person.businessentityaddress (
    "businessentityid" INTEGER NOT NULL,
    "addressid" INTEGER NOT NULL,
    "addresstypeid" INTEGER NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS person.businessentitycontact (
    "businessentityid" INTEGER NOT NULL,
    "personid" INTEGER NOT NULL,
    "contacttypeid" INTEGER NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS person.contacttype (
    "contacttypeid" INTEGER NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS person.countryregion (
    "countryregioncode" VARCHAR(3) NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS person.emailaddress (
    "businessentityid" INTEGER NOT NULL,
    "emailaddressid" INTEGER NOT NULL,
    "emailaddress" VARCHAR(50) NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS person.password (
    "businessentityid" INTEGER NOT NULL,
    "passwordhash" VARCHAR(128) NOT NULL,
    "passwordsalt" VARCHAR(10) NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS person.person (
    "businessentityid" INTEGER NOT NULL,
    "persontype" CHAR(2) NOT NULL,
    "namestyle" BOOLEAN NOT NULL,
    "title" VARCHAR(8) NULL,
    "firstname" VARCHAR(50) NOT NULL,
    "middlename" VARCHAR(50) NULL,
    "lastname" VARCHAR(50) NOT NULL,
    "suffix" VARCHAR(10) NULL,
    "emailpromotion" INTEGER NOT NULL,
    "additionalcontactinfo" XML NULL,
    "demographics" XML NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS person.personphone (
    "businessentityid" INTEGER NOT NULL,
    "phonenumber" VARCHAR(25) NOT NULL,
    "phonenumbertypeid" INTEGER NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS person.phonenumbertype (
    "phonenumbertypeid" INTEGER NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS person.stateprovince (
    "stateprovinceid" INTEGER NOT NULL,
    "stateprovincecode" CHAR(3) NOT NULL,
    "countryregioncode" VARCHAR(3) NOT NULL,
    "isonlystateprovinceflag" BOOLEAN NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "territoryid" INTEGER NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.billofmaterials (
    "billofmaterialsid" INTEGER NOT NULL,
    "productassemblyid" INTEGER NULL,
    "componentid" INTEGER NOT NULL,
    "startdate" TIMESTAMP NOT NULL,
    "enddate" TIMESTAMP NULL,
    "unitmeasurecode" CHAR(3) NOT NULL,
    "bomlevel" SMALLINT NOT NULL,
    "perassemblyqty" NUMERIC(8,2) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.culture (
    "cultureid" CHAR(6) NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.document (
    "documentnode" VARCHAR(100) NOT NULL,
    "documentlevel" SMALLINT NULL,
    "title" VARCHAR(50) NOT NULL,
    "owner" INTEGER NOT NULL,
    "folderflag" BOOLEAN NOT NULL,
    "filename" VARCHAR(400) NOT NULL,
    "fileextension" VARCHAR(8) NOT NULL,
    "revision" CHAR(5) NOT NULL,
    "changenumber" INTEGER NOT NULL,
    "status" SMALLINT NOT NULL,
    "documentsummary" TEXT NULL,
    "document" BYTEA NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.illustration (
    "illustrationid" INTEGER NOT NULL,
    "diagram" XML NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.location (
    "locationid" SMALLINT NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "costrate" NUMERIC(10,4) NOT NULL,
    "availability" NUMERIC(8,2) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.product (
    "productid" INTEGER NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "productnumber" VARCHAR(25) NOT NULL,
    "makeflag" BOOLEAN NOT NULL,
    "finishedgoodsflag" BOOLEAN NOT NULL,
    "color" VARCHAR(15) NULL,
    "safetystocklevel" SMALLINT NOT NULL,
    "reorderpoint" SMALLINT NOT NULL,
    "standardcost" NUMERIC(19,4) NOT NULL,
    "listprice" NUMERIC(19,4) NOT NULL,
    "size" VARCHAR(5) NULL,
    "sizeunitmeasurecode" CHAR(3) NULL,
    "weightunitmeasurecode" CHAR(3) NULL,
    "weight" NUMERIC(8,2) NULL,
    "daystomanufacture" INTEGER NOT NULL,
    "productline" CHAR(2) NULL,
    "class" CHAR(2) NULL,
    "style" CHAR(2) NULL,
    "productsubcategoryid" INTEGER NULL,
    "productmodelid" INTEGER NULL,
    "sellstartdate" TIMESTAMP NOT NULL,
    "sellenddate" TIMESTAMP NULL,
    "discontinueddate" TIMESTAMP NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.productcategory (
    "productcategoryid" INTEGER NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.productcosthistory (
    "productid" INTEGER NOT NULL,
    "startdate" TIMESTAMP NOT NULL,
    "enddate" TIMESTAMP NULL,
    "standardcost" NUMERIC(19,4) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.productdescription (
    "productdescriptionid" INTEGER NOT NULL,
    "description" VARCHAR(400) NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.productdocument (
    "productid" INTEGER NOT NULL,
    "documentnode" VARCHAR(100) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.productinventory (
    "productid" INTEGER NOT NULL,
    "locationid" SMALLINT NOT NULL,
    "shelf" VARCHAR(10) NOT NULL,
    "bin" SMALLINT NOT NULL,
    "quantity" SMALLINT NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.productlistpricehistory (
    "productid" INTEGER NOT NULL,
    "startdate" TIMESTAMP NOT NULL,
    "enddate" TIMESTAMP NULL,
    "listprice" NUMERIC(19,4) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.productmodel (
    "productmodelid" INTEGER NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "catalogdescription" XML NULL,
    "instructions" XML NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.productmodelillustration (
    "productmodelid" INTEGER NOT NULL,
    "illustrationid" INTEGER NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.productmodelproductdescriptionculture (
    "productmodelid" INTEGER NOT NULL,
    "productdescriptionid" INTEGER NOT NULL,
    "cultureid" CHAR(6) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.productphoto (
    "productphotoid" INTEGER NOT NULL,
    "thumbnailphoto" BYTEA NULL,
    "thumbnailphotofilename" VARCHAR(50) NULL,
    "largephoto" BYTEA NULL,
    "largephotofilename" VARCHAR(50) NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.productproductphoto (
    "productid" INTEGER NOT NULL,
    "productphotoid" INTEGER NOT NULL,
    "primary" BOOLEAN NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.productreview (
    "productreviewid" INTEGER NOT NULL,
    "productid" INTEGER NOT NULL,
    "reviewername" VARCHAR(50) NOT NULL,
    "reviewdate" TIMESTAMP NOT NULL,
    "emailaddress" VARCHAR(50) NOT NULL,
    "rating" INTEGER NOT NULL,
    "comments" VARCHAR(3850) NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.productsubcategory (
    "productsubcategoryid" INTEGER NOT NULL,
    "productcategoryid" INTEGER NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.scrapreason (
    "scrapreasonid" SMALLINT NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.transactionhistory (
    "transactionid" INTEGER NOT NULL,
    "productid" INTEGER NOT NULL,
    "referenceorderid" INTEGER NOT NULL,
    "referenceorderlineid" INTEGER NOT NULL,
    "transactiondate" TIMESTAMP NOT NULL,
    "transactiontype" CHAR(1) NOT NULL,
    "quantity" INTEGER NOT NULL,
    "actualcost" NUMERIC(19,4) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.transactionhistoryarchive (
    "transactionid" INTEGER NOT NULL,
    "productid" INTEGER NOT NULL,
    "referenceorderid" INTEGER NOT NULL,
    "referenceorderlineid" INTEGER NOT NULL,
    "transactiondate" TIMESTAMP NOT NULL,
    "transactiontype" CHAR(1) NOT NULL,
    "quantity" INTEGER NOT NULL,
    "actualcost" NUMERIC(19,4) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.unitmeasure (
    "unitmeasurecode" CHAR(3) NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.workorder (
    "workorderid" INTEGER NOT NULL,
    "productid" INTEGER NOT NULL,
    "orderqty" INTEGER NOT NULL,
    "stockedqty" INTEGER NOT NULL,
    "scrappedqty" SMALLINT NOT NULL,
    "startdate" TIMESTAMP NOT NULL,
    "enddate" TIMESTAMP NULL,
    "duedate" TIMESTAMP NOT NULL,
    "scrapreasonid" SMALLINT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS production.workorderrouting (
    "workorderid" INTEGER NOT NULL,
    "productid" INTEGER NOT NULL,
    "operationsequence" SMALLINT NOT NULL,
    "locationid" SMALLINT NOT NULL,
    "scheduledstartdate" TIMESTAMP NOT NULL,
    "scheduledenddate" TIMESTAMP NOT NULL,
    "actualstartdate" TIMESTAMP NULL,
    "actualenddate" TIMESTAMP NULL,
    "actualresourcehrs" NUMERIC(9,4) NULL,
    "plannedcost" NUMERIC(19,4) NOT NULL,
    "actualcost" NUMERIC(19,4) NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS purchasing.productvendor (
    "productid" INTEGER NOT NULL,
    "businessentityid" INTEGER NOT NULL,
    "averageleadtime" INTEGER NOT NULL,
    "standardprice" NUMERIC(19,4) NOT NULL,
    "lastreceiptcost" NUMERIC(19,4) NULL,
    "lastreceiptdate" TIMESTAMP NULL,
    "minorderqty" INTEGER NOT NULL,
    "maxorderqty" INTEGER NOT NULL,
    "onorderqty" INTEGER NULL,
    "unitmeasurecode" CHAR(3) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS purchasing.purchaseorderdetail (
    "purchaseorderid" INTEGER NOT NULL,
    "purchaseorderdetailid" INTEGER NOT NULL,
    "duedate" TIMESTAMP NOT NULL,
    "orderqty" SMALLINT NOT NULL,
    "productid" INTEGER NOT NULL,
    "unitprice" NUMERIC(19,4) NOT NULL,
    "linetotal" NUMERIC(19,4) NOT NULL,
    "receivedqty" NUMERIC(8,2) NOT NULL,
    "rejectedqty" NUMERIC(8,2) NOT NULL,
    "stockedqty" NUMERIC(9,2) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS purchasing.purchaseorderheader (
    "purchaseorderid" INTEGER NOT NULL,
    "revisionnumber" SMALLINT NOT NULL,
    "status" SMALLINT NOT NULL,
    "employeeid" INTEGER NOT NULL,
    "vendorid" INTEGER NOT NULL,
    "shipmethodid" INTEGER NOT NULL,
    "orderdate" TIMESTAMP NOT NULL,
    "shipdate" TIMESTAMP NULL,
    "subtotal" NUMERIC(19,4) NOT NULL,
    "taxamt" NUMERIC(19,4) NOT NULL,
    "freight" NUMERIC(19,4) NOT NULL,
    "totaldue" NUMERIC(19,4) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS purchasing.shipmethod (
    "shipmethodid" INTEGER NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "shipbase" NUMERIC(19,4) NOT NULL,
    "shiprate" NUMERIC(19,4) NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS purchasing.vendor (
    "businessentityid" INTEGER NOT NULL,
    "accountnumber" VARCHAR(15) NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "creditrating" SMALLINT NOT NULL,
    "preferredvendorstatus" BOOLEAN NOT NULL,
    "activeflag" BOOLEAN NOT NULL,
    "purchasingwebserviceurl" VARCHAR(1024) NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.countryregioncurrency (
    "countryregioncode" VARCHAR(3) NOT NULL,
    "currencycode" CHAR(3) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.creditcard (
    "creditcardid" INTEGER NOT NULL,
    "cardtype" VARCHAR(50) NOT NULL,
    "cardnumber" VARCHAR(25) NOT NULL,
    "expmonth" SMALLINT NOT NULL,
    "expyear" SMALLINT NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.currency (
    "currencycode" CHAR(3) NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.currencyrate (
    "currencyrateid" INTEGER NOT NULL,
    "currencyratedate" TIMESTAMP NOT NULL,
    "fromcurrencycode" CHAR(3) NOT NULL,
    "tocurrencycode" CHAR(3) NOT NULL,
    "averagerate" NUMERIC(19,4) NOT NULL,
    "endofdayrate" NUMERIC(19,4) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.customer (
    "customerid" INTEGER NOT NULL,
    "personid" INTEGER NULL,
    "storeid" INTEGER NULL,
    "territoryid" INTEGER NULL,
    "accountnumber" VARCHAR(10) NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.personcreditcard (
    "businessentityid" INTEGER NOT NULL,
    "creditcardid" INTEGER NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.salesorderdetail (
    "salesorderid" INTEGER NOT NULL,
    "salesorderdetailid" INTEGER NOT NULL,
    "carriertrackingnumber" VARCHAR(25) NULL,
    "orderqty" SMALLINT NOT NULL,
    "productid" INTEGER NOT NULL,
    "specialofferid" INTEGER NOT NULL,
    "unitprice" NUMERIC(19,4) NOT NULL,
    "unitpricediscount" NUMERIC(19,4) NOT NULL,
    "linetotal" NUMERIC(38,6) NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.salesorderheader (
    "salesorderid" INTEGER NOT NULL,
    "revisionnumber" SMALLINT NOT NULL,
    "orderdate" TIMESTAMP NOT NULL,
    "duedate" TIMESTAMP NOT NULL,
    "shipdate" TIMESTAMP NULL,
    "status" SMALLINT NOT NULL,
    "onlineorderflag" BOOLEAN NOT NULL,
    "salesordernumber" VARCHAR(25) NOT NULL,
    "purchaseordernumber" VARCHAR(25) NULL,
    "accountnumber" VARCHAR(15) NULL,
    "customerid" INTEGER NOT NULL,
    "salespersonid" INTEGER NULL,
    "territoryid" INTEGER NULL,
    "billtoaddressid" INTEGER NOT NULL,
    "shiptoaddressid" INTEGER NOT NULL,
    "shipmethodid" INTEGER NOT NULL,
    "creditcardid" INTEGER NULL,
    "creditcardapprovalcode" VARCHAR(15) NULL,
    "currencyrateid" INTEGER NULL,
    "subtotal" NUMERIC(19,4) NOT NULL,
    "taxamt" NUMERIC(19,4) NOT NULL,
    "freight" NUMERIC(19,4) NOT NULL,
    "totaldue" NUMERIC(19,4) NOT NULL,
    "comment" VARCHAR(128) NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.salesorderheadersalesreason (
    "salesorderid" INTEGER NOT NULL,
    "salesreasonid" INTEGER NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.salesperson (
    "businessentityid" INTEGER NOT NULL,
    "territoryid" INTEGER NULL,
    "salesquota" NUMERIC(19,4) NULL,
    "bonus" NUMERIC(19,4) NOT NULL,
    "commissionpct" NUMERIC(10,4) NOT NULL,
    "salesytd" NUMERIC(19,4) NOT NULL,
    "saleslastyear" NUMERIC(19,4) NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.salespersonquotahistory (
    "businessentityid" INTEGER NOT NULL,
    "quotadate" TIMESTAMP NOT NULL,
    "salesquota" NUMERIC(19,4) NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.salesreason (
    "salesreasonid" INTEGER NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "reasontype" VARCHAR(50) NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.salestaxrate (
    "salestaxrateid" INTEGER NOT NULL,
    "stateprovinceid" INTEGER NOT NULL,
    "taxtype" SMALLINT NOT NULL,
    "taxrate" NUMERIC(10,4) NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.salesterritory (
    "territoryid" INTEGER NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "countryregioncode" VARCHAR(3) NOT NULL,
    "group" VARCHAR(50) NOT NULL,
    "salesytd" NUMERIC(19,4) NOT NULL,
    "saleslastyear" NUMERIC(19,4) NOT NULL,
    "costytd" NUMERIC(19,4) NOT NULL,
    "costlastyear" NUMERIC(19,4) NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.salesterritoryhistory (
    "businessentityid" INTEGER NOT NULL,
    "territoryid" INTEGER NOT NULL,
    "startdate" TIMESTAMP NOT NULL,
    "enddate" TIMESTAMP NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.shoppingcartitem (
    "shoppingcartitemid" INTEGER NOT NULL,
    "shoppingcartid" VARCHAR(50) NOT NULL,
    "quantity" INTEGER NOT NULL,
    "productid" INTEGER NOT NULL,
    "datecreated" TIMESTAMP NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.specialoffer (
    "specialofferid" INTEGER NOT NULL,
    "description" VARCHAR(255) NOT NULL,
    "discountpct" NUMERIC(10,4) NOT NULL,
    "type" VARCHAR(50) NOT NULL,
    "category" VARCHAR(50) NOT NULL,
    "startdate" TIMESTAMP NOT NULL,
    "enddate" TIMESTAMP NOT NULL,
    "minqty" INTEGER NOT NULL,
    "maxqty" INTEGER NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.specialofferproduct (
    "specialofferid" INTEGER NOT NULL,
    "productid" INTEGER NOT NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales.store (
    "businessentityid" INTEGER NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "salespersonid" INTEGER NULL,
    "demographics" XML NULL,
    "rowguid" UUID NOT NULL,
    "modifieddate" TIMESTAMP NOT NULL
);
