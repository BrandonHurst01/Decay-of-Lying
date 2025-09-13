<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="tei"
    version="1.0">
    
    <!-- Identity transform: copy everything by default -->
    <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()" />
        </xsl:copy>
    </xsl:template>
    
    <!-- Remove <add> elements with change="StC" (drop content too) -->
    <xsl:template match="tei:add[@change='StC' or @change='#StC']" />
    
    <!-- Strip <del> tags with change="StC" but keep their content -->
    <xsl:template match="tei:del[@change='StC' or @change='#StC']">
        <xsl:apply-templates select="node()" />
    </xsl:template>
    
</xsl:stylesheet>
