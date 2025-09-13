<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="tei"
    version="1.0">
    
    <!-- Identity transform -->
    <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()" />
        </xsl:copy>
    </xsl:template>
    
    <!-- 1. Remove <del> elements with change StB or StBa (drop content) -->
    <xsl:template match="tei:del[@change='StB' or @change='#StB' or @change='StBa' or @change='#StBa']" />
    
    <!-- 2. Flatten <add> elements with change StB or StBa (keep content, strip tag) -->
    <xsl:template match="tei:add[@change='StB' or @change='#StB' or @change='StBa' or @change='#StBa']">
        <xsl:apply-templates select="node()" />
    </xsl:template>
    
    <!-- 3. StC deletions & additions are left intact (identity transform already does this) -->
    
</xsl:stylesheet>
