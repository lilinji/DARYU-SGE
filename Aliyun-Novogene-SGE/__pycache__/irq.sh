#!/bin/bash

enable_rps()
{
        ethSet=`ls -d /sys/class/net/eth*`
        for ethd in $ethSet
        do      
		eth=`basename $ethd`
		cur_combined=`ethtool -l $eth 2>/dev/null | grep -i "combined" | tail -n 1 | grep -o "[[:digit:]]"`
		if [ "$?" == "0" -a "$cur_combined" != "1" ]; then 
			echo "current $eth has $cur_combined queue, bypass rps set for it..."
			#echo "current $eth has $cur_combined queue, still do rps set for it..."
			continue	
		fi

		rfc=2048
		cc=$(grep -c processor /proc/cpuinfo) 
		rsfe=$(echo $cc*$rfc | bc) 
		sysctl -w net.core.rps_sock_flow_entries=$rsfe 
		for fileRps in $(ls /sys/class/net/$eth/queues/rx-*/rps_cpus) 
		do
		    echo ff > $fileRps 
		done
		     
		for fileRfc in $(ls /sys/class/net/$eth/queues/rx-*/rps_flow_cnt) 
		do
		    echo $rfc > $fileRfc 
		done
		     
		tail /sys/class/net/$eth/queues/rx-*/{rps_cpus,rps_flow_cnt}
	done
}

enable_mq()
{
        ethSet=`ls -d /sys/class/net/eth*`
        for ethd in $ethSet
        do      
                eth=`basename $ethd`
                pre_max=`ethtool -l $eth 2>/dev/null | grep -i "combined" | head -n 1 | awk '{print $NF}'`
                cur_max=`ethtool -l $eth 2>/dev/null | grep -i "combined" | tail -n 1 | awk '{print $NF}'`

                [ $? -eq 0 ] || continue #ethtool error

                if [ $pre_max -ne $cur_max ]; then
                        ethtool -L $eth combined $pre_max
                        echo "Set [$eth] Current Combined to <$pre_max>"
                fi
        done
}

set_affinity()
{
	VEC=$((VEC%(NUMCORES-1)+1))
        if [ $VEC -ge 32 ]
        then
                MASK_FILL=""
                MASK_ZERO="00000000"
                let "IDX = $VEC / 32"
                for ((i=1; i<=$IDX;i++))
                do
                        MASK_FILL="${MASK_FILL},${MASK_ZERO}"
                done

                let "VEC -= 32 * $IDX"
                let "VEC += 1"
                MASK_TMP=$((1<<($VEC-1) % $NUMCORES))
                MASK=`printf "%X%s" $MASK_TMP $MASK_FILL`
        else
                MASK_TMP=$((1<<($VEC-1) % $NUMCORES))
                MASK=`printf "%X" $MASK_TMP`
        fi

    printf "%s mask=%s for /proc/irq/%d/smp_affinity\n" $DEV $MASK $IRQ
    printf "%s" $MASK > /proc/irq/$IRQ/smp_affinity
}

enable_irq_affinity()
{
	# calculate number of processors
	NUMCORES=`grep processor /proc/cpuinfo | wc -l`
	DEV="octeon"
	DEV="virtio"
	MAX=`grep $DEV /proc/interrupts | wc -l`
	if [ "$MAX" == "0" ] ; then
	  echo no vectors found on $DEV
	  continue
	fi
	for VEC in `seq 0 1 $MAX`
	do
	  IRQ=`cat /proc/interrupts | grep -i $DEV  | cut  -d:  -f1 | sed "s/ //g" | head -$VEC | tail -1`
	  #IRQ=`cat /proc/interrupts | grep -i $DEV"$"  | cut  -d:  -f1 | sed "s/ //g" | head -$VEC | tail -1`
	  if [ -n  "$IRQ" ]; then
	    set_affinity
	  fi
	done
}

if [ "$1" != "" ] ; then
        echo "Description:"
        echo "    This script attempts to bind each queue of a NIC"
        echo "usage:"
        echo "    $0"
        exit
fi


# check for irqbalance running
IRQBALANCE_ON=`ps ax | grep -v grep | grep -q irqbalance; echo $?`
if [ "$IRQBALANCE_ON" == "0" ] ; then
        echo " WARNING: irqbalance is running and will"
        echo "          likely override this script's affinitization."
        echo "          Please stop the irqbalance service and/or execute"
        echo "          'killall irqbalance'"
fi


enable_mq
enable_rps
enable_irq_affinity
