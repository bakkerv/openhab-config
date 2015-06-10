<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

   <xsl:output indent="yes" method="xml" encoding="UTF-8" omit-xml-declaration="yes" />

<xsl:template match="/">

 <xsl:value-of select="//appliance[name='Wasmachine']/logs/point_log[type='electricity_consumed']//measurement">

</xsl:template>
</xsl:stylesheet>
